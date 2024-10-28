# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains directives that can be used within a package.

Directives are functions that can be called inside a package
definition to modify the package, for example:

    class OpenMpi(Package):
        depends_on("hwloc")
        provides("mpi")
        ...

``provides`` and ``depends_on`` are spack directives.

The available directives are:

  * ``build_system``
  * ``conflicts``
  * ``depends_on``
  * ``extends``
  * ``patch``
  * ``provides``
  * ``resource``
  * ``variant``
  * ``version``
  * ``requires``
  * ``redistribute``

"""
import collections
import collections.abc
import os.path
import re
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Tuple, Union

import llnl.util.lang
import llnl.util.tty.color

import spack.deptypes as dt
import spack.patch
import spack.spec
import spack.util.crypto
import spack.variant
from spack.dependency import Dependency
from spack.directives_meta import DirectiveError, DirectiveMeta
from spack.fetch_strategy import from_kwargs
from spack.resource import Resource
from spack.version import (
    GitVersion,
    Version,
    VersionChecksumError,
    VersionError,
    VersionLookupError,
)

if TYPE_CHECKING:
    import spack.package_base

__all__ = [
    "DirectiveError",
    "DirectiveMeta",
    "DisableRedistribute",
    "version",
    "conflicts",
    "depends_on",
    "extends",
    "maintainers",
    "license",
    "provides",
    "patch",
    "variant",
    "resource",
    "build_system",
    "requires",
    "redistribute",
]

_patch_order_index = 0


SpecType = str
DepType = Union[Tuple[str, ...], str]
WhenType = Optional[Union["spack.spec.Spec", str, bool]]
Patcher = Callable[[Union["spack.package_base.PackageBase", Dependency]], None]
PatchesType = Optional[Union[Patcher, str, List[Union[Patcher, str]]]]


SUPPORTED_LANGUAGES = ("fortran", "cxx", "c")


def _make_when_spec(value: WhenType) -> Optional["spack.spec.Spec"]:
    """Create a ``Spec`` that indicates when a directive should be applied.

    Directives with ``when`` specs, e.g.:

        patch('foo.patch', when='@4.5.1:')
        depends_on('mpi', when='+mpi')
        depends_on('readline', when=sys.platform() != 'darwin')

    are applied conditionally depending on the value of the ``when``
    keyword argument.  Specifically:

      1. If the ``when`` argument is ``True``, the directive is always applied
      2. If it is ``False``, the directive is never applied
      3. If it is a ``Spec`` string, it is applied when the package's
         concrete spec satisfies the ``when`` spec.

    The first two conditions are useful for the third example case above.
    It allows package authors to include directives that are conditional
    at package definition time, in additional to ones that are evaluated
    as part of concretization.

    Arguments:
        value: a conditional Spec, constant ``bool``, or None if not supplied
           value indicating when a directive should be applied.

    """
    if isinstance(value, spack.spec.Spec):
        return value

    # Unsatisfiable conditions are discarded by the caller, and never
    # added to the package class
    if value is False:
        return None

    # If there is no constraint, the directive should always apply;
    # represent this by returning the unconstrained `Spec()`, which is
    # always satisfied.
    if value is None or value is True:
        return spack.spec.Spec()

    # This is conditional on the spec
    return spack.spec.Spec(value)


SubmoduleCallback = Callable[["spack.package_base.PackageBase"], Union[str, List[str], bool]]
directive = DirectiveMeta.directive


@directive("versions")
def version(
    ver: Union[str, int],
    # this positional argument is deprecated, use sha256=... instead
    checksum: Optional[str] = None,
    *,
    # generic version options
    preferred: Optional[bool] = None,
    deprecated: Optional[bool] = None,
    no_cache: Optional[bool] = None,
    # url fetch options
    url: Optional[str] = None,
    extension: Optional[str] = None,
    expand: Optional[bool] = None,
    fetch_options: Optional[dict] = None,
    # url archive verification options
    md5: Optional[str] = None,
    sha1: Optional[str] = None,
    sha224: Optional[str] = None,
    sha256: Optional[str] = None,
    sha384: Optional[str] = None,
    sha512: Optional[str] = None,
    # git fetch options
    git: Optional[str] = None,
    commit: Optional[str] = None,
    tag: Optional[str] = None,
    branch: Optional[str] = None,
    get_full_repo: Optional[bool] = None,
    submodules: Union[SubmoduleCallback, Optional[bool]] = None,
    submodules_delete: Optional[bool] = None,
    # other version control
    svn: Optional[str] = None,
    hg: Optional[str] = None,
    cvs: Optional[str] = None,
    revision: Optional[str] = None,
    date: Optional[str] = None,
):
    """Adds a version and, if appropriate, metadata for fetching its code.

    The ``version`` directives are aggregated into a ``versions`` dictionary
    attribute with ``Version`` keys and metadata values, where the metadata
    is stored as a dictionary of ``kwargs``.

    The (keyword) arguments are turned into a valid fetch strategy for
    code packages later. See ``spack.fetch_strategy.for_package_version()``.
    """
    kwargs = {
        key: value
        for key, value in (
            ("sha256", sha256),
            ("sha384", sha384),
            ("sha512", sha512),
            ("preferred", preferred),
            ("deprecated", deprecated),
            ("expand", expand),
            ("url", url),
            ("extension", extension),
            ("no_cache", no_cache),
            ("fetch_options", fetch_options),
            ("git", git),
            ("svn", svn),
            ("hg", hg),
            ("cvs", cvs),
            ("get_full_repo", get_full_repo),
            ("branch", branch),
            ("submodules", submodules),
            ("submodules_delete", submodules_delete),
            ("commit", commit),
            ("tag", tag),
            ("revision", revision),
            ("date", date),
            ("md5", md5),
            ("sha1", sha1),
            ("sha224", sha224),
            ("checksum", checksum),
        )
        if value is not None
    }
    return lambda pkg: _execute_version(pkg, ver, **kwargs)


def _execute_version(pkg, ver, **kwargs):
    if (
        (any(s in kwargs for s in spack.util.crypto.hashes) or "checksum" in kwargs)
        and hasattr(pkg, "has_code")
        and not pkg.has_code
    ):
        raise VersionChecksumError(
            "{0}: Checksums not allowed in no-code packages "
            "(see '{1}' version).".format(pkg.name, ver)
        )

    if not isinstance(ver, (int, str)):
        raise VersionError(
            f"{pkg.name}: declared version '{ver!r}' in package should be a string or int."
        )

    # Declared versions are concrete
    version = Version(ver)

    if isinstance(version, GitVersion) and not hasattr(pkg, "git") and "git" not in kwargs:
        args = ", ".join(f"{argname}='{value}'" for argname, value in kwargs.items())
        raise VersionLookupError(
            f"{pkg.name}: spack version directives cannot include git hashes fetched from URLs.\n"
            f"    version('{ver}', {args})"
        )

    # Store kwargs for the package to later with a fetch_strategy.
    pkg.versions[version] = kwargs


def _depends_on(
    pkg: "spack.package_base.PackageBase",
    spec: "spack.spec.Spec",
    *,
    when: WhenType = None,
    type: DepType = dt.DEFAULT_TYPES,
    patches: PatchesType = None,
):
    when_spec = _make_when_spec(when)
    if not when_spec:
        return

    if not spec.name:
        raise DependencyError(f"Invalid dependency specification in package '{pkg.name}':", spec)
    if pkg.name == spec.name:
        raise CircularReferenceError(f"Package '{pkg.name}' cannot depend on itself.")

    depflag = dt.canonicalize(type)

    # call this patches here for clarity -- we want patch to be a list,
    # but the caller doesn't have to make it one.

    # Note: we cannot check whether a package is virtual in a directive
    # because directives are run as part of class instantiation, and specs
    # instantiate the package class as part of the `virtual` check.
    # To be technical, specs only instantiate the package class as part of the
    # virtual check if the provider index hasn't been created yet.
    # TODO: There could be a cache warming strategy that would allow us to
    # ensure `Spec.virtual` is a valid thing to call in a directive.
    # For now, we comment out the following check to allow for virtual packages
    # with package files.
    # if patches and spec.virtual:
    #     raise DependencyPatchError("Cannot patch a virtual dependency.")

    # ensure patches is a list
    if patches is None:
        patches = []
    elif not isinstance(patches, (list, tuple)):
        patches = [patches]

    # auto-call patch() directive on any strings in patch list
    patches = [patch(p) if isinstance(p, str) else p for p in patches]
    assert all(callable(p) for p in patches)

    # this is where we actually add the dependency to this package
    deps_by_name = pkg.dependencies.setdefault(when_spec, {})
    dependency = deps_by_name.get(spec.name)

    if not dependency:
        dependency = Dependency(pkg, spec, depflag=depflag)
        deps_by_name[spec.name] = dependency
    else:
        dependency.spec.constrain(spec, deps=False)
        dependency.depflag |= depflag

    # apply patches to the dependency
    for execute_patch in patches:
        execute_patch(dependency)


@directive("conflicts")
def conflicts(conflict_spec: SpecType, when: WhenType = None, msg: Optional[str] = None):
    """Allows a package to define a conflict.

    Currently, a "conflict" is a concretized configuration that is known
    to be non-valid. For example, a package that is known not to be
    buildable with intel compilers can declare::

        conflicts('%intel')

    To express the same constraint only when the 'foo' variant is
    activated::

        conflicts('%intel', when='+foo')

    Args:
        conflict_spec (spack.spec.Spec): constraint defining the known conflict
        when (spack.spec.Spec): optional constraint that triggers the conflict
        msg (str): optional user defined message
    """

    def _execute_conflicts(pkg: "spack.package_base.PackageBase"):
        # If when is not specified the conflict always holds
        when_spec = _make_when_spec(when)
        if not when_spec:
            return

        # Save in a list the conflicts and the associated custom messages
        conflict_spec_list = pkg.conflicts.setdefault(when_spec, [])
        msg_with_name = f"{pkg.name}: {msg}" if msg is not None else msg
        conflict_spec_list.append((spack.spec.Spec(conflict_spec), msg_with_name))

    return _execute_conflicts


@directive(("dependencies"))
def depends_on(
    spec: SpecType,
    when: WhenType = None,
    type: DepType = dt.DEFAULT_TYPES,
    patches: PatchesType = None,
):
    """Creates a dict of deps with specs defining when they apply.

    Args:
        spec: the package and constraints depended on
        when: when the dependent satisfies this, it has
            the dependency represented by ``spec``
        type: str or tuple of legal Spack deptypes
        patches: single result of ``patch()`` directive, a
            ``str`` to be passed to ``patch``, or a list of these

    This directive is to be used inside a Package definition to declare
    that the package requires other packages to be built first.
    @see The section "Dependency specs" in the Spack Packaging Guide.

    """
    dep_spec = spack.spec.Spec(spec)
    if dep_spec.name in SUPPORTED_LANGUAGES:
        assert type == "build", "languages must be of 'build' type"
        return _language(lang_spec_str=spec, when=when)

    def _execute_depends_on(pkg: "spack.package_base.PackageBase"):
        _depends_on(pkg, dep_spec, when=when, type=type, patches=patches)

    return _execute_depends_on


#: Store whether a given Spec source/binary should not be redistributed.
class DisableRedistribute:
    def __init__(self, source, binary):
        self.source = source
        self.binary = binary


@directive("disable_redistribute")
def redistribute(source=None, binary=None, when: WhenType = None):
    """Can be used inside a Package definition to declare that
    the package source and/or compiled binaries should not be
    redistributed.

    By default, Packages allow source/binary distribution (i.e. in
    mirrors). Because of this, and because overlapping enable/
    disable specs are not allowed, this directive only allows users
    to explicitly disable redistribution for specs.
    """

    return lambda pkg: _execute_redistribute(pkg, source, binary, when)


def _execute_redistribute(
    pkg: "spack.package_base.PackageBase", source=None, binary=None, when: WhenType = None
):
    if source is None and binary is None:
        return
    elif (source is True) or (binary is True):
        raise DirectiveError(
            "Source/binary distribution are true by default, they can only "
            "be explicitly disabled."
        )

    if source is None:
        source = True
    if binary is None:
        binary = True

    when_spec = _make_when_spec(when)
    if not when_spec:
        return
    if source is False:
        max_constraint = spack.spec.Spec(f"{pkg.name}@{when_spec.versions}")
        if not max_constraint.satisfies(when_spec):
            raise DirectiveError("Source distribution can only be disabled for versions")

    if when_spec in pkg.disable_redistribute:
        disable = pkg.disable_redistribute[when_spec]
        if not source:
            disable.source = True
        if not binary:
            disable.binary = True
    else:
        pkg.disable_redistribute[when_spec] = DisableRedistribute(
            source=not source, binary=not binary
        )


@directive(("extendees", "dependencies"))
def extends(spec, when=None, type=("build", "run"), patches=None):
    """Same as depends_on, but also adds this package to the extendee list.
    In case of Python, also adds a dependency on python-venv.

    keyword arguments can be passed to extends() so that extension
    packages can pass parameters to the extendee's extension
    mechanism."""

    def _execute_extends(pkg):
        when_spec = _make_when_spec(when)
        if not when_spec:
            return

        dep_spec = spack.spec.Spec(spec)

        _depends_on(pkg, dep_spec, when=when, type=type, patches=patches)

        # When extending python, also add a dependency on python-venv. This is done so that
        # Spack environment views are Python virtual environments.
        if dep_spec.name == "python" and not pkg.name == "python-venv":
            _depends_on(pkg, spack.spec.Spec("python-venv"), when=when, type=("build", "run"))

        # TODO: the values of the extendees dictionary are not used. Remove in next refactor.
        pkg.extendees[dep_spec.name] = (dep_spec, None)

    return _execute_extends


@directive(dicts=("provided", "provided_together"))
def provides(*specs: SpecType, when: WhenType = None):
    """Allows packages to provide a virtual dependency.

    If a package provides "mpi", other packages can declare that they depend on "mpi",
    and spack can use the providing package to satisfy the dependency.

    Args:
        *specs: virtual specs provided by this package
        when: condition when this provides clause needs to be considered
    """

    def _execute_provides(pkg: "spack.package_base.PackageBase"):
        import spack.parser  # Avoid circular dependency

        when_spec = _make_when_spec(when)
        if not when_spec:
            return

        # ``when`` specs for ``provides()`` need a name, as they are used
        # to build the ProviderIndex.
        when_spec.name = pkg.name

        spec_objs = [spack.spec.Spec(x) for x in specs]
        spec_names = [x.name for x in spec_objs]
        if len(spec_names) > 1:
            pkg.provided_together.setdefault(when_spec, []).append(set(spec_names))

        for provided_spec in spec_objs:
            if pkg.name == provided_spec.name:
                raise CircularReferenceError("Package '%s' cannot provide itself." % pkg.name)

            provided_set = pkg.provided.setdefault(when_spec, set())
            provided_set.add(provided_spec)

    return _execute_provides


@directive("patches")
def patch(
    url_or_filename: str,
    level: int = 1,
    when: WhenType = None,
    working_dir: str = ".",
    reverse: bool = False,
    sha256: Optional[str] = None,
    archive_sha256: Optional[str] = None,
) -> Patcher:
    """Packages can declare patches to apply to source.  You can
    optionally provide a when spec to indicate that a particular
    patch should only be applied when the package's spec meets
    certain conditions (e.g. a particular version).

    Args:
        url_or_filename: url or relative filename of the patch
        level: patch level (as in the patch shell command)
        when: optional anonymous spec that specifies when to apply the patch
        working_dir: dir to change to before applying
        reverse: reverse the patch
        sha256: sha256 sum of the patch, used to verify the patch (only required for URL patches)
        archive_sha256: sha256 sum of the *archive*, if the patch is compressed (only required for
            compressed URL patches)
    """

    def _execute_patch(pkg_or_dep: Union["spack.package_base.PackageBase", Dependency]):
        pkg = pkg_or_dep
        if isinstance(pkg, Dependency):
            pkg = pkg.pkg

        if hasattr(pkg, "has_code") and not pkg.has_code:
            raise UnsupportedPackageDirective(
                "Patches are not allowed in {0}: package has no code.".format(pkg.name)
            )

        when_spec = _make_when_spec(when)
        if not when_spec:
            return

        # If this spec is identical to some other, then append this
        # patch to the existing list.
        cur_patches = pkg_or_dep.patches.setdefault(when_spec, [])

        global _patch_order_index
        ordering_key = (pkg.name, _patch_order_index)
        _patch_order_index += 1

        patch: spack.patch.Patch
        if "://" in url_or_filename:
            if sha256 is None:
                raise ValueError("patch() with a url requires a sha256")

            patch = spack.patch.UrlPatch(
                pkg,
                url_or_filename,
                level,
                working_dir=working_dir,
                reverse=reverse,
                ordering_key=ordering_key,
                sha256=sha256,
                archive_sha256=archive_sha256,
            )
        else:
            patch = spack.patch.FilePatch(
                pkg, url_or_filename, level, working_dir, reverse, ordering_key=ordering_key
            )

        cur_patches.append(patch)

    return _execute_patch


@directive("variants")
def variant(
    name: str,
    default: Optional[Any] = None,
    description: str = "",
    values: Optional[Union[collections.abc.Sequence, Callable[[Any], bool]]] = None,
    multi: Optional[bool] = None,
    validator: Optional[Callable[[str, str, Tuple[Any, ...]], None]] = None,
    when: Optional[Union[str, bool]] = None,
    sticky: bool = False,
):
    """Define a variant for the package.

    Packager can specify a default value as well as a text description.

    Args:
        name: Name of the variant
        default: Default value for the variant, if not specified otherwise the default will be
            False for a boolean variant and 'nothing' for a multi-valued variant
        description: Description of the purpose of the variant
        values: Either a tuple of strings containing the allowed values, or a callable accepting
            one value and returning True if it is valid
        multi: If False only one value per spec is allowed for this variant
        validator: Optional group validator to enforce additional logic. It receives the package
            name, the variant name and a tuple of values and should raise an instance of SpackError
            if the group doesn't meet the additional constraints
        when: Optional condition on which the variant applies
        sticky: The variant should not be changed by the concretizer to find a valid concrete spec

    Raises:
        DirectiveError: If arguments passed to the directive are invalid
    """

    def format_error(msg, pkg):
        msg += " @*r{{[{0}, variant '{1}']}}"
        return llnl.util.tty.color.colorize(msg.format(pkg.name, name))

    if name in spack.variant.reserved_names:

        def _raise_reserved_name(pkg):
            msg = "The name '%s' is reserved by Spack" % name
            raise DirectiveError(format_error(msg, pkg))

        return _raise_reserved_name

    # Ensure we have a sequence of allowed variant values, or a
    # predicate for it.
    if values is None:
        if str(default).upper() in ("TRUE", "FALSE"):
            values = (True, False)
        else:
            values = lambda x: True

    # The object defining variant values might supply its own defaults for
    # all the other arguments. Ensure we have no conflicting definitions
    # in place.
    for argument in ("default", "multi", "validator"):
        # TODO: we can consider treating 'default' differently from other
        # TODO: attributes and let a packager decide whether to use the fluent
        # TODO: interface or the directive argument
        if hasattr(values, argument) and locals()[argument] is not None:

            def _raise_argument_error(pkg):
                msg = (
                    "Remove specification of {0} argument: it is handled "
                    "by an attribute of the 'values' argument"
                )
                raise DirectiveError(format_error(msg.format(argument), pkg))

            return _raise_argument_error

    # Allow for the object defining the allowed values to supply its own
    # default value and group validator, say if it supports multiple values.
    default = getattr(values, "default", default)
    validator = getattr(values, "validator", validator)
    multi = getattr(values, "multi", bool(multi))

    # Here we sanitize against a default value being either None
    # or the empty string, as the former indicates that a default
    # was not set while the latter will make the variant unparsable
    # from the command line
    if default is None or default == "":

        def _raise_default_not_set(pkg):
            if default is None:
                msg = "either a default was not explicitly set, " "or 'None' was used"
            elif default == "":
                msg = "the default cannot be an empty string"
            raise DirectiveError(format_error(msg, pkg))

        return _raise_default_not_set

    description = str(description).strip()

    def _execute_variant(pkg):
        when_spec = _make_when_spec(when)

        if not re.match(spack.spec.IDENTIFIER_RE, name):
            directive = "variant"
            msg = "Invalid variant name in {0}: '{1}'"
            raise DirectiveError(directive, msg.format(pkg.name, name))

        # variants are stored by condition then by name (so only the last variant of a
        # given name takes precedence *per condition*).
        # NOTE: variant defaults and values can conflict if when conditions overlap.
        variants_by_name = pkg.variants.setdefault(when_spec, {})
        variants_by_name[name] = spack.variant.Variant(
            name=name,
            default=default,
            description=description,
            values=values,
            multi=multi,
            validator=validator,
            sticky=sticky,
            precedence=pkg.num_variant_definitions(),
        )

    return _execute_variant


@directive("resources")
def resource(**kwargs):
    """Define an external resource to be fetched and staged when building the
    package. Based on the keywords present in the dictionary the appropriate
    FetchStrategy will be used for the resource. Resources are fetched and
    staged in their own folder inside spack stage area, and then moved into
    the stage area of the package that needs them.

    List of recognized keywords:

    * 'when' : (optional) represents the condition upon which the resource is
      needed
    * 'destination' : (optional) path where to move the resource. This path
      must be relative to the main package stage area.
    * 'placement' : (optional) gives the possibility to fine tune how the
      resource is moved into the main package stage area.
    """

    def _execute_resource(pkg):
        when = kwargs.get("when")
        when_spec = _make_when_spec(when)
        if not when_spec:
            return

        destination = kwargs.get("destination", "")
        placement = kwargs.get("placement", None)

        # Check if the path is relative
        if os.path.isabs(destination):
            message = (
                "The destination keyword of a resource directive " "can't be an absolute path.\n"
            )
            message += "\tdestination : '{dest}\n'".format(dest=destination)
            raise RuntimeError(message)

        # Check if the path falls within the main package stage area
        test_path = "stage_folder_root"
        normalized_destination = os.path.normpath(
            os.path.join(test_path, destination)
        )  # Normalized absolute path

        if test_path not in normalized_destination:
            message = (
                "The destination folder of a resource must fall "
                "within the main package stage directory.\n"
            )
            message += "\tdestination : '{dest}'\n".format(dest=destination)
            raise RuntimeError(message)

        resources = pkg.resources.setdefault(when_spec, [])
        name = kwargs.get("name")
        fetcher = from_kwargs(**kwargs)
        resources.append(Resource(name, fetcher, destination, placement))

    return _execute_resource


def build_system(*values, **kwargs):
    default = kwargs.get("default", None) or values[0]
    return variant(
        "build_system",
        values=tuple(values),
        description="Build systems supported by the package",
        default=default,
        multi=False,
    )


@directive(dicts=())
def maintainers(*names: str):
    """Add a new maintainer directive, to specify maintainers in a declarative way.

    Args:
        names: GitHub username for the maintainer
    """

    def _execute_maintainer(pkg):
        maintainers = set(getattr(pkg, "maintainers", []))
        maintainers.update(names)
        pkg.maintainers = sorted(maintainers)

    return _execute_maintainer


def _execute_license(pkg, license_identifier: str, when):
    # If when is not specified the license always holds
    when_spec = _make_when_spec(when)
    if not when_spec:
        return

    for other_when_spec in pkg.licenses:
        if when_spec.intersects(other_when_spec):
            when_message = ""
            if when_spec != _make_when_spec(None):
                when_message = f"when {when_spec}"
            other_when_message = ""
            if other_when_spec != _make_when_spec(None):
                other_when_message = f"when {other_when_spec}"
            err_msg = (
                f"{pkg.name} is specified as being licensed as {license_identifier} "
                f"{when_message}, but it is also specified as being licensed under "
                f"{pkg.licenses[other_when_spec]} {other_when_message}, which conflict."
            )
            raise OverlappingLicenseError(err_msg)

    pkg.licenses[when_spec] = license_identifier


@directive("licenses")
def license(
    license_identifier: str,
    checked_by: Optional[Union[str, List[str]]] = None,
    when: Optional[Union[str, bool]] = None,
):
    """Add a new license directive, to specify the SPDX identifier the software is
    distributed under.

    Args:
        license_identifiers: SPDX identifier specifying the license(s) the software
            is distributed under.
        checked_by: string or list of strings indicating which github user checked the
            license (if any).
        when: A spec specifying when the license applies.
    """

    return lambda pkg: _execute_license(pkg, license_identifier, when)


@directive("requirements")
def requires(*requirement_specs: str, policy="one_of", when=None, msg=None):
    """Allows a package to request a configuration to be present in all valid solutions.

    For instance, a package that is known to compile only with GCC can declare:

        requires("%gcc")

    A package that requires Apple-Clang on Darwin can declare instead:

        requires("%apple-clang", when="platform=darwin", msg="Apple Clang is required on Darwin")

    Args:
        requirement_specs: spec expressing the requirement
        when: optional constraint that triggers the requirement. If None the requirement
            is applied unconditionally.

        msg: optional user defined message
    """

    def _execute_requires(pkg: "spack.package_base.PackageBase"):
        if policy not in ("one_of", "any_of"):
            err_msg = (
                f"the 'policy' argument of the 'requires' directive in {pkg.name} is set "
                f"to a wrong value (only 'one_of' or 'any_of' are allowed)"
            )
            raise DirectiveError(err_msg)

        when_spec = _make_when_spec(when)
        if not when_spec:
            return

        # Save in a list the requirements and the associated custom messages
        requirement_list = pkg.requirements.setdefault(when_spec, [])
        msg_with_name = f"{pkg.name}: {msg}" if msg is not None else msg
        requirements = tuple(spack.spec.Spec(s) for s in requirement_specs)
        requirement_list.append((requirements, policy, msg_with_name))

    return _execute_requires


@directive("languages")
def _language(lang_spec_str: str, *, when: Optional[Union[str, bool]] = None):
    """Temporary implementation of language virtuals, until compilers are proper dependencies."""

    def _execute_languages(pkg: "spack.package_base.PackageBase"):
        when_spec = _make_when_spec(when)
        if not when_spec:
            return

        languages = pkg.languages.setdefault(when_spec, set())
        languages.add(lang_spec_str)

    return _execute_languages


class DependencyError(DirectiveError):
    """This is raised when a dependency specification is invalid."""


class CircularReferenceError(DependencyError):
    """This is raised when something depends on itself."""


class DependencyPatchError(DirectiveError):
    """Raised for errors with patching dependencies."""


class UnsupportedPackageDirective(DirectiveError):
    """Raised when an invalid or unsupported package directive is specified."""


class OverlappingLicenseError(DirectiveError):
    """Raised when two licenses are declared that apply on overlapping specs."""
