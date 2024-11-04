# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from http.client import HTTPResponse
from typing import List, NamedTuple, Tuple
from urllib.request import Request

import llnl.util.tty as tty

import spack.fetch_strategy
import spack.mirror
import spack.oci.opener
import spack.stage
import spack.util.url

from .image import Digest, ImageReference


class Blob(NamedTuple):
    compressed_digest: Digest
    uncompressed_digest: Digest
    size: int


def with_query_param(url: str, param: str, value: str) -> str:
    """Add a query parameter to a URL

    Args:
        url: The URL to add the parameter to.
        param: The parameter name.
        value: The parameter value.

    Returns:
        The URL with the parameter added.
    """
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    if param in query:
        query[param].append(value)
    else:
        query[param] = [value]
    return urllib.parse.urlunparse(
        parsed._replace(query=urllib.parse.urlencode(query, doseq=True))
    )


def list_tags(ref: ImageReference, _urlopen: spack.oci.opener.MaybeOpen = None) -> List[str]:
    """Retrieves the list of tags associated with an image, handling pagination."""
    _urlopen = _urlopen or spack.oci.opener.urlopen
    tags = set()
    fetch_url = ref.tags_url()

    while True:
        # Fetch tags
        request = Request(url=fetch_url)
        response = _urlopen(request)
        spack.oci.opener.ensure_status(request, response, 200)
        tags.update(json.load(response)["tags"])

        # Check for pagination
        link_header = response.headers["Link"]

        if link_header is None:
            break

        tty.debug(f"OCI tag pagination: {link_header}")

        rel_next_value = spack.util.url.parse_link_rel_next(link_header)

        if rel_next_value is None:
            break

        rel_next = urllib.parse.urlparse(rel_next_value)

        if rel_next.scheme not in ("https", ""):
            break

        fetch_url = ref.endpoint(rel_next_value)

    return sorted(tags)


def upload_blob(
    ref: ImageReference,
    file: str,
    digest: Digest,
    force: bool = False,
    small_file_size: int = 0,
    _urlopen: spack.oci.opener.MaybeOpen = None,
) -> bool:
    """Uploads a blob to an OCI registry

    We only do monolithic uploads, even though it's very simple to do chunked.
    Observed problems with chunked uploads:
    (1) it's slow, many sequential requests, (2) some registries set an *unknown*
    max chunk size, and the spec doesn't say how to obtain it

    Args:
        ref: The image reference.
        file: The file to upload.
        digest: The digest of the file.
        force: Whether to force upload the blob, even if it already exists.
        small_file_size: For files at most this size, attempt
            to do a single POST request instead of POST + PUT.
            Some registries do no support single requests, and others
            do not specify what size they support in single POST.
            For now this feature is disabled by default (0KB)

    Returns:
        True if the blob was uploaded, False if it already existed.
    """
    _urlopen = _urlopen or spack.oci.opener.urlopen

    # Test if the blob already exists, if so, early exit.
    if not force and blob_exists(ref, digest, _urlopen):
        return False

    with open(file, "rb") as f:
        file_size = os.fstat(f.fileno()).st_size

        # For small blobs, do a single POST request.
        # The spec says that registries MAY support this
        if file_size <= small_file_size:
            request = Request(
                url=ref.uploads_url(digest),
                method="POST",
                data=f,
                headers={
                    "Content-Type": "application/octet-stream",
                    "Content-Length": str(file_size),
                },
            )
        else:
            request = Request(
                url=ref.uploads_url(), method="POST", headers={"Content-Length": "0"}
            )

        response = _urlopen(request)

        # Created the blob in one go.
        if response.status == 201:
            return True

        # Otherwise, do another PUT request.
        spack.oci.opener.ensure_status(request, response, 202)
        assert "Location" in response.headers

        # Can be absolute or relative, joining handles both
        upload_url = with_query_param(
            ref.endpoint(response.headers["Location"]), "digest", str(digest)
        )
        f.seek(0)

        request = Request(
            url=upload_url,
            method="PUT",
            data=f,
            headers={"Content-Type": "application/octet-stream", "Content-Length": str(file_size)},
        )

        response = _urlopen(request)

        spack.oci.opener.ensure_status(request, response, 201)

    return True


def upload_manifest(
    ref: ImageReference,
    manifest: dict,
    tag: bool = True,
    _urlopen: spack.oci.opener.MaybeOpen = None,
):
    """Uploads a manifest/index to a registry

    Args:
        ref: The image reference.
        manifest: The manifest or index.
        tag: When true, use the tag, otherwise use the digest,
            this is relevant for multi-arch images, where the
            tag is an index, referencing the manifests by digest.

    Returns:
        The digest and size of the uploaded manifest.
    """
    _urlopen = _urlopen or spack.oci.opener.urlopen

    data = json.dumps(manifest, separators=(",", ":")).encode()
    digest = Digest.from_sha256(hashlib.sha256(data).hexdigest())
    size = len(data)

    if not tag:
        ref = ref.with_digest(digest)

    request = Request(
        url=ref.manifest_url(),
        method="PUT",
        data=data,
        headers={"Content-Type": manifest["mediaType"]},
    )

    response = _urlopen(request)

    spack.oci.opener.ensure_status(request, response, 201)
    return digest, size


def image_from_mirror(mirror: spack.mirror.Mirror) -> ImageReference:
    """Given an OCI based mirror, extract the URL and image name from it"""
    url = mirror.push_url
    if not url.startswith("oci://"):
        raise ValueError(f"Mirror {mirror} is not an OCI mirror")
    return ImageReference.from_string(url[6:])


def blob_exists(
    ref: ImageReference, digest: Digest, _urlopen: spack.oci.opener.MaybeOpen = None
) -> bool:
    """Checks if a blob exists in an OCI registry"""
    try:
        _urlopen = _urlopen or spack.oci.opener.urlopen
        response = _urlopen(Request(url=ref.blob_url(digest), method="HEAD"))
        return response.status == 200
    except urllib.error.HTTPError as e:
        if e.getcode() == 404:
            return False
        raise


def copy_missing_layers(
    src: ImageReference,
    dst: ImageReference,
    architecture: str,
    _urlopen: spack.oci.opener.MaybeOpen = None,
) -> Tuple[dict, dict]:
    """Copy image layers from src to dst for given architecture.

    Args:
        src: The source image reference.
        dst: The destination image reference.
        architecture: The architecture (when referencing an index)

    Returns:
        Tuple of manifest and config of the base image.
    """
    _urlopen = _urlopen or spack.oci.opener.urlopen
    manifest, config = get_manifest_and_config(src, architecture, _urlopen=_urlopen)

    # Get layer digests
    digests = [Digest.from_string(layer["digest"]) for layer in manifest["layers"]]

    # Filter digests that are don't exist in the registry
    missing_digests = [
        digest for digest in digests if not blob_exists(dst, digest, _urlopen=_urlopen)
    ]

    if not missing_digests:
        return manifest, config

    # Pull missing blobs, push them to the registry
    with spack.stage.StageComposite.from_iterable(
        make_stage(url=src.blob_url(digest), digest=digest, _urlopen=_urlopen)
        for digest in missing_digests
    ) as stages:
        stages.fetch()
        stages.check()
        stages.cache_local()

        for stage, digest in zip(stages, missing_digests):
            # No need to check existince again, force=True.
            upload_blob(
                dst, file=stage.save_filename, force=True, digest=digest, _urlopen=_urlopen
            )

    return manifest, config


#: OCI manifest content types (including docker type)
manifest_content_type = [
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.v2+json",
]

#: OCI index content types (including docker type)
index_content_type = [
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
]

#: All OCI manifest / index content types
all_content_type = manifest_content_type + index_content_type


def get_manifest_and_config(
    ref: ImageReference,
    architecture="amd64",
    recurse=3,
    _urlopen: spack.oci.opener.MaybeOpen = None,
) -> Tuple[dict, dict]:
    """Recursively fetch manifest and config for a given image reference
    with a given architecture.

    Args:
        ref: The image reference.
        architecture: The architecture (when referencing an index)
        recurse: How many levels of index to recurse into.

    Returns:
        A tuple of (manifest, config)"""

    _urlopen = _urlopen or spack.oci.opener.urlopen

    # Get manifest
    response: HTTPResponse = _urlopen(
        Request(url=ref.manifest_url(), headers={"Accept": ", ".join(all_content_type)})
    )

    # Recurse when we find an index
    if response.headers["Content-Type"] in index_content_type:
        if recurse == 0:
            raise Exception("Maximum recursion depth reached while fetching OCI manifest")

        index = json.load(response)
        manifest_meta = next(
            manifest
            for manifest in index["manifests"]
            if manifest["platform"]["architecture"] == architecture
        )

        return get_manifest_and_config(
            ref.with_digest(manifest_meta["digest"]),
            architecture=architecture,
            recurse=recurse - 1,
            _urlopen=_urlopen,
        )

    # Otherwise, require a manifest
    if response.headers["Content-Type"] not in manifest_content_type:
        raise Exception(f"Unknown content type {response.headers['Content-Type']}")

    manifest = json.load(response)

    # Download, verify and cache config file
    config_digest = Digest.from_string(manifest["config"]["digest"])
    with make_stage(ref.blob_url(config_digest), config_digest, _urlopen=_urlopen) as stage:
        stage.fetch()
        stage.check()
        stage.cache_local()
        with open(stage.save_filename, "rb") as f:
            config = json.load(f)

    return manifest, config


#: Same as upload_manifest, but with retry wrapper
upload_manifest_with_retry = spack.oci.opener.default_retry(upload_manifest)

#: Same as upload_blob, but with retry wrapper
upload_blob_with_retry = spack.oci.opener.default_retry(upload_blob)

#: Same as get_manifest_and_config, but with retry wrapper
get_manifest_and_config_with_retry = spack.oci.opener.default_retry(get_manifest_and_config)

#: Same as copy_missing_layers, but with retry wrapper
copy_missing_layers_with_retry = spack.oci.opener.default_retry(copy_missing_layers)


def make_stage(
    url: str, digest: Digest, keep: bool = False, _urlopen: spack.oci.opener.MaybeOpen = None
) -> spack.stage.Stage:
    _urlopen = _urlopen or spack.oci.opener.urlopen
    fetch_strategy = spack.fetch_strategy.OCIRegistryFetchStrategy(
        url=url, checksum=digest.digest, _urlopen=_urlopen
    )
    # Use blobs/<alg>/<encoded> as the cache path, which follows
    # the OCI Image Layout Specification. What's missing though,
    # is the `oci-layout` and `index.json` files, which are
    # required by the spec.
    return spack.stage.Stage(
        fetch_strategy, mirror_paths=spack.mirror.OCILayout(digest), name=digest.digest, keep=keep
    )
