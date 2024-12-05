# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
This file contains code for creating spack mirror directories.  A
mirror is an organized hierarchy containing specially named archive
files.  This enabled spack to know where to find files in a mirror if
the main server for a particular package is down.  Or, if the computer
where spack is run is not connected to the internet, it allows spack
to download packages directly from a mirror (e.g., on an intranet).
"""
import os
import os.path
import sys
import traceback
from typing import Optional

import llnl.url
import llnl.util.symlink
import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.caches
import spack.config
import spack.error
import spack.fetch_strategy
import spack.mirror
import spack.oci.image
import spack.repo
import spack.spec
import spack.util.spack_yaml as syaml
import spack.version
from spack.error import MirrorError
from spack.mirrors.mirror import Mirror, MirrorCollection


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


def get_all_versions(specs):
    """Given a set of initial specs, return a new set of specs that includes
    each version of each package in the original set.

    Note that if any spec in the original set specifies properties other than
    version, this information will be omitted in the new set; for example; the
    new set of specs will not include variant settings.
    """
    version_specs = []
    for spec in specs:
        pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
        # Skip any package that has no known versions.
        if not pkg_cls.versions:
            tty.msg("No safe (checksummed) versions for package %s" % pkg_cls.name)
            continue

        for version in pkg_cls.versions:
            version_spec = spack.spec.Spec(pkg_cls.name)
            version_spec.versions = spack.version.VersionList([version])
            version_specs.append(version_spec)

    return version_specs


def get_matching_versions(specs, num_versions=1):
    """Get a spec for EACH known version matching any spec in the list.
    For concrete specs, this retrieves the concrete version and, if more
    than one version per spec is requested, retrieves the latest versions
    of the package.
    """
    matching = []
    for spec in specs:
        pkg = spec.package

        # Skip any package that has no known versions.
        if not pkg.versions:
            tty.msg("No safe (checksummed) versions for package %s" % pkg.name)
            continue

        pkg_versions = num_versions

        version_order = list(reversed(sorted(pkg.versions)))
        matching_spec = []
        if spec.concrete:
            matching_spec.append(spec)
            pkg_versions -= 1
            if spec.version in version_order:
                version_order.remove(spec.version)

        for v in version_order:
            # Generate no more than num_versions versions for each spec.
            if pkg_versions < 1:
                break

            # Generate only versions that satisfy the spec.
            if spec.concrete or v.intersects(spec.versions):
                s = spack.spec.Spec(pkg.name)
                s.versions = spack.version.VersionList([v])
                s.variants = spec.variants.copy()
                # This is needed to avoid hanging references during the
                # concretization phase
                s.variants.spec = s
                matching_spec.append(s)
                pkg_versions -= 1

        if not matching_spec:
            tty.warn("No known version matches spec: %s" % spec)
        matching.extend(matching_spec)

    return matching


def create(path, specs, skip_unstable_versions=False):
    """Create a directory to be used as a spack mirror, and fill it with
    package archives.

    Arguments:
        path: Path to create a mirror directory hierarchy in.
        specs: Any package versions matching these specs will be added \
            to the mirror.
        skip_unstable_versions: if true, this skips adding resources when
            they do not have a stable archive checksum (as determined by
            ``fetch_strategy.stable_target``)

    Return Value:
        Returns a tuple of lists: (present, mirrored, error)

        * present:  Package specs that were already present.
        * mirrored: Package specs that were successfully mirrored.
        * error:    Package specs that failed to mirror due to some error.
    """
    # automatically spec-ify anything in the specs array.
    specs = [s if isinstance(s, spack.spec.Spec) else spack.spec.Spec(s) for s in specs]

    mirror_cache, mirror_stats = mirror_cache_and_stats(path, skip_unstable_versions)
    for spec in specs:
        mirror_stats.next_spec(spec)
        create_mirror_from_package_object(spec.package, mirror_cache, mirror_stats)

    return mirror_stats.stats()


def mirror_cache_and_stats(path, skip_unstable_versions=False):
    """Return both a mirror cache and a mirror stats, starting from the path
    where a mirror ought to be created.

    Args:
        path (str): path to create a mirror directory hierarchy in.
        skip_unstable_versions: if true, this skips adding resources when
            they do not have a stable archive checksum (as determined by
            ``fetch_strategy.stable_target``)
    """
    # Get the absolute path of the root before we start jumping around.
    if not os.path.isdir(path):
        try:
            mkdirp(path)
        except OSError as e:
            raise MirrorError("Cannot create directory '%s':" % path, str(e))
    mirror_cache = spack.caches.MirrorCache(path, skip_unstable_versions=skip_unstable_versions)
    mirror_stats = MirrorStats()
    return mirror_cache, mirror_stats


def add(mirror: Mirror, scope=None):
    """Add a named mirror in the given scope"""
    mirrors = spack.config.get("mirrors", scope=scope)
    if not mirrors:
        mirrors = syaml.syaml_dict()

    if mirror.name in mirrors:
        tty.die("Mirror with name {} already exists.".format(mirror.name))

    items = [(n, u) for n, u in mirrors.items()]
    items.insert(0, (mirror.name, mirror.to_dict()))
    mirrors = syaml.syaml_dict(items)
    spack.config.set("mirrors", mirrors, scope=scope)


def remove(name, scope):
    """Remove the named mirror in the given scope"""
    mirrors = spack.config.get("mirrors", scope=scope)
    if not mirrors:
        mirrors = syaml.syaml_dict()

    if name not in mirrors:
        tty.die("No mirror with name %s" % name)

    mirrors.pop(name)
    spack.config.set("mirrors", mirrors, scope=scope)
    tty.msg("Removed mirror %s." % name)


class MirrorStats:
    def __init__(self):
        self.present = {}
        self.new = {}
        self.errors = set()

        self.current_spec = None
        self.added_resources = set()
        self.existing_resources = set()

    def next_spec(self, spec):
        self._tally_current_spec()
        self.current_spec = spec

    def _tally_current_spec(self):
        if self.current_spec:
            if self.added_resources:
                self.new[self.current_spec] = len(self.added_resources)
            if self.existing_resources:
                self.present[self.current_spec] = len(self.existing_resources)
            self.added_resources = set()
            self.existing_resources = set()
        self.current_spec = None

    def stats(self):
        self._tally_current_spec()
        return list(self.present), list(self.new), list(self.errors)

    def already_existed(self, resource):
        # If an error occurred after caching a subset of a spec's
        # resources, a secondary attempt may consider them already added
        if resource not in self.added_resources:
            self.existing_resources.add(resource)

    def added(self, resource):
        self.added_resources.add(resource)

    def error(self):
        self.errors.add(self.current_spec)


def create_mirror_from_package_object(pkg_obj, mirror_cache, mirror_stats):
    """Add a single package object to a mirror.

    The package object is only required to have an associated spec
    with a concrete version.

    Args:
        pkg_obj (spack.package_base.PackageBase): package object with to be added.
        mirror_cache (spack.caches.MirrorCache): mirror where to add the spec.
        mirror_stats (spack.mirror.MirrorStats): statistics on the current mirror

    Return:
        True if the spec was added successfully, False otherwise
    """
    tty.msg("Adding package {} to mirror".format(pkg_obj.spec.format("{name}{@version}")))
    num_retries = 3
    while num_retries > 0:
        try:
            # Includes patches and resources
            with pkg_obj.stage as pkg_stage:
                pkg_stage.cache_mirror(mirror_cache, mirror_stats)
            exception = None
            break
        except Exception as e:
            exc_tuple = sys.exc_info()
            exception = e
        num_retries -= 1
    if exception:
        if spack.config.get("config:debug"):
            traceback.print_exception(file=sys.stderr, *exc_tuple)
        else:
            tty.warn(
                "Error while fetching %s" % pkg_obj.spec.cformat("{name}{@version}"),
                getattr(exception, "message", exception),
            )
        mirror_stats.error()
        return False
    return True


def require_mirror_name(mirror_name):
    """Find a mirror by name and raise if it does not exist"""
    mirror = MirrorCollection().get(mirror_name)
    if not mirror:
        raise ValueError(f'no mirror named "{mirror_name}"')
    return mirror
