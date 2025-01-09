# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import stat
import warnings

import spack.config
import spack.error
import spack.repo
import spack.spec
from spack.error import ConfigError
from spack.version import Version

_lesser_spec_types = {"compiler": spack.spec.CompilerSpec, "version": Version}


def _spec_type(component):
    """Map from component name to spec type for package prefs."""
    return _lesser_spec_types.get(component, spack.spec.Spec)


class PackagePrefs:
    """Defines the sort order for a set of specs.

    Spack's package preference implementation uses PackagePrefss to
    define sort order. The PackagePrefs class looks at Spack's
    packages.yaml configuration and, when called on a spec, returns a key
    that can be used to sort that spec in order of the user's
    preferences.

    You can use it like this:

       # key function sorts CompilerSpecs for `mpich` in order of preference
       kf = PackagePrefs('mpich', 'compiler')
       compiler_list.sort(key=kf)

    Or like this:

       # key function to sort VersionLists for OpenMPI in order of preference.
       kf = PackagePrefs('openmpi', 'version')
       version_list.sort(key=kf)

    Optionally, you can sort in order of preferred virtual dependency
    providers.  To do that, provide 'providers' and a third argument
    denoting the virtual package (e.g., ``mpi``):

       kf = PackagePrefs('trilinos', 'providers', 'mpi')
       provider_spec_list.sort(key=kf)

    """

    def __init__(self, pkgname, component, vpkg=None, all=True):
        self.pkgname = pkgname
        self.component = component
        self.vpkg = vpkg
        self.all = all

        self._spec_order = None

    def __call__(self, spec):
        """Return a key object (an index) that can be used to sort spec.

        Sort is done in package order. We don't cache the result of
        this function as Python's sort functions already ensure that the
        key function is called at most once per sorted element.
        """
        if self._spec_order is None:
            self._spec_order = self._specs_for_pkg(
                self.pkgname, self.component, self.vpkg, self.all
            )
        spec_order = self._spec_order

        # integer is the index of the first spec in order that satisfies
        # spec, or it's a number larger than any position in the order.
        match_index = next(
            (i for i, s in enumerate(spec_order) if spec.intersects(s)), len(spec_order)
        )
        if match_index < len(spec_order) and spec_order[match_index] == spec:
            # If this is called with multiple specs that all satisfy the same
            # minimum index in spec_order, the one which matches that element
            # of spec_order exactly is considered slightly better. Note
            # that because this decreases the value by less than 1, it is not
            # better than a match which occurs at an earlier index.
            match_index -= 0.5
        return match_index

    @classmethod
    def order_for_package(cls, pkgname, component, vpkg=None, all=True):
        """Given a package name, sort component (e.g, version, compiler, ...),
        and an optional vpkg, return the list from the packages config.
        """
        pkglist = [pkgname]
        if all:
            pkglist.append("all")

        for pkg in pkglist:
            pkg_entry = spack.config.get("packages").get(pkg)
            if not pkg_entry:
                continue

            order = pkg_entry.get(component)
            if not order:
                continue

            # vpkg is one more level
            if vpkg is not None:
                order = order.get(vpkg)

            if order:
                ret = [str(s).strip() for s in order]
                if component == "target":
                    ret = ["target=%s" % tname for tname in ret]
                return ret

        return []

    @classmethod
    def _specs_for_pkg(cls, pkgname, component, vpkg=None, all=True):
        """Given a sort order specified by the pkgname/component/second_key,
        return a list of CompilerSpecs, VersionLists, or Specs for
        that sorting list.
        """
        pkglist = cls.order_for_package(pkgname, component, vpkg, all)
        spec_type = _spec_type(component)
        return [spec_type(s) for s in pkglist]

    @classmethod
    def has_preferred_providers(cls, pkgname, vpkg):
        """Whether specific package has a preferred vpkg providers."""
        return bool(cls.order_for_package(pkgname, "providers", vpkg, False))

    @classmethod
    def has_preferred_targets(cls, pkg_name):
        """Whether specific package has a preferred vpkg providers."""
        return bool(cls.order_for_package(pkg_name, "target"))

    @classmethod
    def preferred_variants(cls, pkg_name):
        """Return a VariantMap of preferred variants/values for a spec."""
        for pkg_cls in (pkg_name, "all"):
            variants = spack.config.get("packages").get(pkg_cls, {}).get("variants", "")
            if variants:
                break

        # allow variants to be list or string
        if not isinstance(variants, str):
            variants = " ".join(variants)

        # Only return variants that are actually supported by the package
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        spec = spack.spec.Spec(f"{pkg_name} {variants}")
        return {
            name: variant
            for name, variant in spec.variants.items()
            if name in pkg_cls.variant_names()
        }


def is_spec_buildable(spec):
    """Return true if the spec is configured as buildable"""
    allpkgs = spack.config.get("packages")
    all_buildable = allpkgs.get("all", {}).get("buildable", True)
    so_far = all_buildable  # the default "so far"

    def _package(s):
        pkg_cls = spack.repo.PATH.get_pkg_class(s.name)
        return pkg_cls(s)

    # check whether any providers for this package override the default
    if any(
        _package(spec).provides(name) and entry.get("buildable", so_far) != so_far
        for name, entry in allpkgs.items()
    ):
        so_far = not so_far

    spec_buildable = allpkgs.get(spec.name, {}).get("buildable", so_far)
    return spec_buildable


def get_package_dir_permissions(spec):
    """Return the permissions configured for the spec.

    Include the GID bit if group permissions are on. This makes the group
    attribute sticky for the directory. Package-specific settings take
    precedent over settings for ``all``"""
    perms = get_package_permissions(spec)
    if perms & stat.S_IRWXG and spack.config.get("config:allow_sgid", True):
        perms |= stat.S_ISGID
        if spec.concrete and "/afs/" in spec.prefix:
            warnings.warn(
                "Directory {0} seems to be located on AFS. If you"
                " encounter errors, try disabling the allow_sgid option"
                " using: spack config add 'config:allow_sgid:false'".format(spec.prefix)
            )
    return perms


def get_package_permissions(spec):
    """Return the permissions configured for the spec.

    Package-specific settings take precedence over settings for ``all``"""

    # Get read permissions level
    for name in (spec.name, "all"):
        try:
            readable = spack.config.get("packages:%s:permissions:read" % name, "")
            if readable:
                break
        except AttributeError:
            readable = "world"

    # Get write permissions level
    for name in (spec.name, "all"):
        try:
            writable = spack.config.get("packages:%s:permissions:write" % name, "")
            if writable:
                break
        except AttributeError:
            writable = "user"

    perms = stat.S_IRWXU
    if readable in ("world", "group"):  # world includes group
        perms |= stat.S_IRGRP | stat.S_IXGRP
    if readable == "world":
        perms |= stat.S_IROTH | stat.S_IXOTH

    if writable in ("world", "group"):
        if readable == "user":
            raise ConfigError(
                "Writable permissions may not be more"
                + " permissive than readable permissions.\n"
                + "      Violating package is %s" % spec.name
            )
        perms |= stat.S_IWGRP
    if writable == "world":
        if readable != "world":
            raise ConfigError(
                "Writable permissions may not be more"
                + " permissive than readable permissions.\n"
                + "      Violating package is %s" % spec.name
            )
        perms |= stat.S_IWOTH

    return perms


def get_package_group(spec):
    """Return the unix group associated with the spec.

    Package-specific settings take precedence over settings for ``all``"""
    for name in (spec.name, "all"):
        try:
            group = spack.config.get("packages:%s:permissions:group" % name, "")
            if group:
                break
        except AttributeError:
            group = ""
    return group


class VirtualInPackagesYAMLError(spack.error.SpackError):
    """Raised when a disallowed virtual is found in packages.yaml"""
