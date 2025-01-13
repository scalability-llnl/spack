# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import traceback

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.caches
import spack.config
import spack.error
import spack.repo
import spack.spec
import spack.util.spack_yaml as syaml
import spack.version
from spack.error import MirrorError
from spack.mirrors.mirror import Mirror, MirrorCollection


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


def create_mirror_from_package_object(
    pkg_obj, mirror_cache: "spack.caches.MirrorCache", mirror_stats: MirrorStats
) -> bool:
    """Add a single package object to a mirror.

    The package object is only required to have an associated spec
    with a concrete version.

    Args:
        pkg_obj (spack.package_base.PackageBase): package object with to be added.
        mirror_cache: mirror where to add the spec.
        mirror_stats: statistics on the current mirror

    Return:
        True if the spec was added successfully, False otherwise
    """
    tty.msg("Adding package {} to mirror".format(pkg_obj.spec.format("{name}{@version}")))
    max_retries = 3
    for num_retries in range(max_retries):
        try:
            # Includes patches and resources
            with pkg_obj.stage as pkg_stage:
                pkg_stage.cache_mirror(mirror_cache, mirror_stats)
            break
        except Exception as e:
            if num_retries + 1 == max_retries:
                if spack.config.get("config:debug"):
                    traceback.print_exc()
                else:
                    tty.warn(
                        "Error while fetching %s" % pkg_obj.spec.format("{name}{@version}"), str(e)
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
