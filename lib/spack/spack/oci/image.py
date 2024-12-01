# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import urllib.parse
from typing import Optional, Union

import spack.spec

# notice: Docker is more strict (no uppercase allowed). We parse image names *with* uppercase
# and normalize, so: example.com/Organization/Name -> example.com/organization/name. Tags are
# case sensitive though.
alphanumeric_with_uppercase = r"[a-zA-Z0-9]+"
separator = r"(?:[._]|__|[-]+)"
localhost = r"localhost"
domainNameComponent = r"(?:[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])"
optionalPort = r"(?::[0-9]+)?"
tag = r"[\w][\w.-]{0,127}"
digestPat = r"[A-Za-z][A-Za-z0-9]*(?:[-_+.][A-Za-z][A-Za-z0-9]*)*[:][0-9a-fA-F]{32,}"
ipv6address = r"\[(?:[a-fA-F0-9:]+)\]"

# domain name
domainName = rf"{domainNameComponent}(?:\.{domainNameComponent})*"
host = rf"(?:{domainName}|{ipv6address})"
domainAndPort = rf"{host}{optionalPort}"

# image name
pathComponent = rf"{alphanumeric_with_uppercase}(?:{separator}{alphanumeric_with_uppercase})*"
remoteName = rf"{pathComponent}(?:\/{pathComponent})*"
namePat = rf"(?:{domainAndPort}\/)?{remoteName}"

# Regex for a full image reference, with 3 groups: name, tag, digest
referencePat = re.compile(rf"^({namePat})(?::({tag}))?(?:@({digestPat}))?$")

# Regex for splitting the name into domain and path components
anchoredNameRegexp = re.compile(rf"^(?:({domainAndPort})\/)?({remoteName})$")


def ensure_sha256_checksum(oci_blob: str):
    """Validate that the reference is of the format sha256:<checksum>
    Return the checksum if valid, raise ValueError otherwise."""
    if ":" not in oci_blob:
        raise ValueError(f"Invalid OCI blob format: {oci_blob}")
    alg, checksum = oci_blob.split(":", 1)
    if alg != "sha256":
        raise ValueError(f"Unsupported OCI blob checksum algorithm: {alg}")
    if len(checksum) != 64:
        raise ValueError(f"Invalid OCI blob checksum length: {len(checksum)}")
    return checksum


class Digest:
    """Represents a digest in the format <algorithm>:<digest>.
    Currently only supports sha256 digests."""

    __slots__ = ["algorithm", "digest"]

    def __init__(self, *, algorithm: str, digest: str) -> None:
        self.algorithm = algorithm
        self.digest = digest

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Digest):
            return NotImplemented
        return self.algorithm == __value.algorithm and self.digest == __value.digest

    @classmethod
    def from_string(cls, string: str) -> "Digest":
        return cls(algorithm="sha256", digest=ensure_sha256_checksum(string))

    @classmethod
    def from_sha256(cls, digest: str) -> "Digest":
        return cls(algorithm="sha256", digest=digest)

    def __str__(self) -> str:
        return f"{self.algorithm}:{self.digest}"


class ImageReference:
    """A parsed image of the form domain/name:tag[@digest].
    The digest is optional, and domain and tag are automatically
    filled out with defaults when parsed from string."""

    __slots__ = ["domain", "name", "tag", "digest"]

    def __init__(
        self, *, domain: str, name: str, tag: str = "latest", digest: Optional[Digest] = None
    ):
        self.domain = domain
        self.name = name
        self.tag = tag
        self.digest = digest

    @classmethod
    def from_string(cls, string) -> "ImageReference":
        match = referencePat.match(string)
        if not match:
            raise ValueError(f"Invalid image reference: {string}")

        image, tag, digest = match.groups()

        assert isinstance(image, str)
        assert isinstance(tag, (str, type(None)))
        assert isinstance(digest, (str, type(None)))

        match = anchoredNameRegexp.match(image)

        # This can never happen, since the regex is implied
        # by the regex above. It's just here to make mypy happy.
        assert match, f"Invalid image reference: {string}"

        domain, name = match.groups()

        assert isinstance(domain, (str, type(None)))
        assert isinstance(name, str)

        # Fill out defaults like docker would do...
        # Based on github.com/distribution/distribution: allow short names like "ubuntu"
        # and "user/repo" to be interpreted as "library/ubuntu" and "user/repo:latest
        # Not sure if Spack should follow Docker, but it's what people expect...
        if not domain:
            domain = "index.docker.io"
            name = f"library/{name}"
        elif (
            "." not in domain
            and ":" not in domain
            and domain != "localhost"
            and domain == domain.lower()
        ):
            name = f"{domain}/{name}"
            domain = "index.docker.io"

        # Lowercase the image name. This is enforced by Docker, although the OCI spec isn't clear?
        # We do this anyways, cause for example in Github Actions the <organization>/<repository>
        # part can have uppercase, and may be interpolated when specifying the relevant OCI image.
        name = name.lower()

        if not tag:
            tag = "latest"

        # sha256 is currently the only algorithm that
        # we implement, even though the spec allows for more
        if isinstance(digest, str):
            digest = Digest.from_string(digest)

        return cls(domain=domain, name=name, tag=tag, digest=digest)

    def manifest_url(self) -> str:
        digest_or_tag = self.digest or self.tag
        return f"https://{self.domain}/v2/{self.name}/manifests/{digest_or_tag}"

    def blob_url(self, digest: Union[str, Digest]) -> str:
        if isinstance(digest, str):
            digest = Digest.from_string(digest)
        return f"https://{self.domain}/v2/{self.name}/blobs/{digest}"

    def with_digest(self, digest: Union[str, Digest]) -> "ImageReference":
        if isinstance(digest, str):
            digest = Digest.from_string(digest)
        return ImageReference(domain=self.domain, name=self.name, tag=self.tag, digest=digest)

    def with_tag(self, tag: str) -> "ImageReference":
        return ImageReference(domain=self.domain, name=self.name, tag=tag, digest=self.digest)

    def uploads_url(self, digest: Optional[Digest] = None) -> str:
        url = f"https://{self.domain}/v2/{self.name}/blobs/uploads/"
        if digest:
            url += f"?digest={digest}"
        return url

    def tags_url(self) -> str:
        return f"https://{self.domain}/v2/{self.name}/tags/list"

    def endpoint(self, path: str = "") -> str:
        return urllib.parse.urljoin(f"https://{self.domain}/v2/", path)

    def __str__(self) -> str:
        s = f"{self.domain}/{self.name}"
        if self.tag:
            s += f":{self.tag}"
        if self.digest:
            s += f"@{self.digest}"
        return s

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ImageReference):
            return NotImplemented
        return (
            self.domain == __value.domain
            and self.name == __value.name
            and self.tag == __value.tag
            and self.digest == __value.digest
        )


def _ensure_valid_tag(tag: str) -> str:
    """Ensure a tag is valid for an OCI registry."""
    sanitized = re.sub(r"[^\w.-]", "_", tag)
    if len(sanitized) > 128:
        return sanitized[:64] + sanitized[-64:]
    return sanitized


def default_tag(spec: "spack.spec.Spec") -> str:
    """Return a valid, default image tag for a spec."""
    return _ensure_valid_tag(f"{spec.name}-{spec.version}-{spec.dag_hash()}.spack")


#: Default OCI index tag
default_index_tag = "index.spack"


def tag_is_spec(tag: str) -> bool:
    """Check if a tag is likely a Spec"""
    return tag.endswith(".spack") and tag != default_index_tag


def default_config(architecture: str, os: str):
    return {
        "architecture": architecture,
        "os": os,
        "rootfs": {"type": "layers", "diff_ids": []},
        "config": {"Env": []},
    }


def default_manifest():
    return {
        "mediaType": "application/vnd.oci.image.manifest.v1+json",
        "schemaVersion": 2,
        "config": {"mediaType": "application/vnd.oci.image.config.v1+json"},
        "layers": [],
    }
