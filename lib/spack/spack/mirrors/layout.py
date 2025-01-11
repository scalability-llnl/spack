# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
from typing import Optional

import llnl.url
import llnl.util.symlink
from llnl.util.filesystem import mkdirp

import spack.fetch_strategy
import spack.oci.image
import spack.repo
import spack.spec
from spack.error import MirrorError


class MirrorLayout:
    """A ``MirrorLayout`` object describes the relative path of a mirror entry."""

    def __init__(self, path: str) -> None:
        self.path = path

    def __iter__(self):
        """Yield all paths including aliases where the resource can be found."""
        yield self.path

    def make_alias(self, root: str) -> None:
        """Make the entry ``root / self.path`` available under a human readable alias"""
        pass


class DefaultLayout(MirrorLayout):
    def __init__(self, alias_path: str, digest_path: Optional[str] = None) -> None:
        # When we have a digest, it is used as the primary storage location. If not, then we use
        # the human-readable alias. In case of mirrors of a VCS checkout, we currently do not have
        # a digest, that's why an alias is required and a digest optional.
        super().__init__(path=digest_path or alias_path)
        self.alias = alias_path
        self.digest_path = digest_path

    def make_alias(self, root: str) -> None:
        """Symlink a human readible path in our mirror to the actual storage location."""
        # We already use the human-readable path as the main storage location.
        if not self.digest_path:
            return

        alias, digest = os.path.join(root, self.alias), os.path.join(root, self.digest_path)

        alias_dir = os.path.dirname(alias)
        relative_dst = os.path.relpath(digest, start=alias_dir)

        mkdirp(alias_dir)
        tmp = f"{alias}.tmp"
        llnl.util.symlink.symlink(relative_dst, tmp)

        try:
            os.rename(tmp, alias)
        except OSError:
            # Clean up the temporary if possible
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

    def __iter__(self):
        if self.digest_path:
            yield self.digest_path
        yield self.alias


class OCILayout(MirrorLayout):
    """Follow the OCI Image Layout Specification to archive blobs where paths are of the form
    ``blobs/<algorithm>/<digest>``"""

    def __init__(self, digest: spack.oci.image.Digest) -> None:
        super().__init__(os.path.join("blobs", digest.algorithm, digest.digest))


def _determine_extension(fetcher):
    if isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy):
        if fetcher.expand_archive:
            # If we fetch with a URLFetchStrategy, use URL's archive type
            ext = llnl.url.determine_url_file_extension(fetcher.url)

            if ext:
                # Remove any leading dots
                ext = ext.lstrip(".")
            else:
                msg = """\
Unable to parse extension from {0}.

If this URL is for a tarball but does not include the file extension
in the name, you can explicitly declare it with the following syntax:

    version('1.2.3', 'hash', extension='tar.gz')

If this URL is for a download like a .jar or .whl that does not need
to be expanded, or an uncompressed installation script, you can tell
Spack not to expand it with the following syntax:

    version('1.2.3', 'hash', expand=False)
"""
                raise MirrorError(msg.format(fetcher.url))
        else:
            # If the archive shouldn't be expanded, don't check extension.
            ext = None
    else:
        # Otherwise we'll make a .tar.gz ourselves
        ext = "tar.gz"

    return ext


def default_mirror_layout(
    fetcher: "spack.fetch_strategy.FetchStrategy",
    per_package_ref: str,
    spec: Optional["spack.spec.Spec"] = None,
) -> MirrorLayout:
    """Returns a ``MirrorReference`` object which keeps track of the relative
    storage path of the resource associated with the specified ``fetcher``."""
    ext = None
    if spec:
        pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
        versions = pkg_cls.versions.get(spec.version, {})
        ext = versions.get("extension", None)
    # If the spec does not explicitly specify an extension (the default case),
    # then try to determine it automatically. An extension can only be
    # specified for the primary source of the package (e.g. the source code
    # identified in the 'version' declaration). Resources/patches don't have
    # an option to specify an extension, so it must be inferred for those.
    ext = ext or _determine_extension(fetcher)

    if ext:
        per_package_ref += ".%s" % ext

    global_ref = fetcher.mirror_id()
    if global_ref:
        global_ref = os.path.join("_source-cache", global_ref)
    if global_ref and ext:
        global_ref += ".%s" % ext

    return DefaultLayout(per_package_ref, global_ref)
