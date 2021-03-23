# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This is where most of the action happens in Spack.

The spack package class structure is based strongly on Homebrew
(http://brew.sh/), mainly because Homebrew makes it very easy to create
packages.

"""
import base64
import collections
import contextlib
import copy
import functools
import hashlib
import inspect
import os
import re
import shutil
import sys
import textwrap
import time
import traceback
import six
import types
from typing import Optional, List, Dict, Any, Callable  # novm

import llnl.util.filesystem as fsys
import llnl.util.tty as tty

import spack.compilers
import spack.config
import spack.dependency
import spack.directives
import spack.directory_layout
import spack.error
import spack.fetch_strategy as fs
import spack.hooks
import spack.mirror
import spack.mixins
import spack.multimethod
import spack.paths
import spack.repo
import spack.store
import spack.url
import spack.util.environment
import spack.util.web
from llnl.util.lang import memoized
from llnl.util.link_tree import LinkTree
from ordereddict_backport import OrderedDict
from spack.filesystem_view import YamlFilesystemView
from spack.installer import PackageInstaller, InstallError
from spack.install_test import TestFailure, TestSuite
from spack.util.executable import which, ProcessError
from spack.util.prefix import Prefix
from spack.stage import stage_prefix, Stage, ResourceStage, StageComposite
from spack.util.package_hash import package_hash
from spack.version import Version

"""Allowed URL schemes for spack packages."""
_ALLOWED_URL_SCHEMES = ["http", "https", "ftp", "file", "git"]


# Filename for the Spack build/install log.
_spack_build_logfile = 'spack-build-out.txt'

# Filename for the Spack build/install environment file.
_spack_build_envfile = 'spack-build-env.txt'

# Filename for the Spack configure args file.
_spack_configure_argsfile = 'spack-configure-args.txt'


class InstallPhase(object):
    """Manages a single phase of the installation.

    This descriptor stores at creation time the name of the method it should
    search for execution. The method is retrieved at __get__ time, so that
    it can be overridden by subclasses of whatever class declared the phases.

    It also provides hooks to execute arbitrary callbacks before and after
    the phase.
    """

    def __init__(self, name):
        self.name = name
        self.run_before = []
        self.run_after = []

    def __get__(self, instance, owner):
        # The caller is a class that is trying to customize
        # my behavior adding something
        if instance is None:
            return self
        # If instance is there the caller wants to execute the
        # install phase, thus return a properly set wrapper
        phase = getattr(instance, self.name)

        @functools.wraps(phase)
        def phase_wrapper(spec, prefix):
            # Check instance attributes at the beginning of a phase
            self._on_phase_start(instance)
            # Execute phase pre-conditions,
            # and give them the chance to fail
            for callback in self.run_before:
                callback(instance)
            phase(spec, prefix)
            # Execute phase sanity_checks,
            # and give them the chance to fail
            for callback in self.run_after:
                callback(instance)
            # Check instance attributes at the end of a phase
            self._on_phase_exit(instance)
        return phase_wrapper

    def _on_phase_start(self, instance):
        # If a phase has a matching stop_before_phase attribute,
        # stop the installation process raising a StopPhase
        if getattr(instance, 'stop_before_phase', None) == self.name:
            from spack.build_environment import StopPhase
            raise StopPhase('Stopping before \'{0}\' phase'.format(self.name))

    def _on_phase_exit(self, instance):
        # If a phase has a matching last_phase attribute,
        # stop the installation process raising a StopPhase
        if getattr(instance, 'last_phase', None) == self.name:
            from spack.build_environment import StopPhase
            raise StopPhase('Stopping at \'{0}\' phase'.format(self.name))

    def copy(self):
        try:
            return copy.deepcopy(self)
        except TypeError:
            # This bug-fix was not back-ported in Python 2.6
            # http://bugs.python.org/issue1515
            other = InstallPhase(self.name)
            other.run_before.extend(self.run_before)
            other.run_after.extend(self.run_after)
            return other


#: Registers which are the detectable packages, by repo and package name
#: Need a pass of package repositories to be filled.
detectable_packages = collections.defaultdict(list)


class DetectablePackageMeta(object):
    """Check if a package is detectable and add default implementations
    for the detection function.
    """
    def __init__(cls, name, bases, attr_dict):
        # If a package has the executables attribute then it's
        # assumed to be detectable
        if hasattr(cls, 'executables'):
            @classmethod
            def determine_spec_details(cls, prefix, exes_in_prefix):
                """Allow ``spack external find ...`` to locate installations.

                Args:
                    prefix (str): the directory containing the executables
                    exes_in_prefix (set): the executables that match the regex

                Returns:
                    The list of detected specs for this package
                """
                exes_by_version = collections.defaultdict(list)
                # The default filter function is the identity function for the
                # list of executables
                filter_fn = getattr(cls, 'filter_detected_exes',
                                    lambda x, exes: exes)
                exes_in_prefix = filter_fn(prefix, exes_in_prefix)
                for exe in exes_in_prefix:
                    try:
                        version_str = cls.determine_version(exe)
                        if version_str:
                            exes_by_version[version_str].append(exe)
                    except Exception as e:
                        msg = ('An error occurred when trying to detect '
                               'the version of "{0}" [{1}]')
                        tty.debug(msg.format(exe, str(e)))

                specs = []
                for version_str, exes in exes_by_version.items():
                    variants = cls.determine_variants(exes, version_str)
                    # Normalize output to list
                    if not isinstance(variants, list):
                        variants = [variants]

                    for variant in variants:
                        if isinstance(variant, six.string_types):
                            variant = (variant, {})
                        variant_str, extra_attributes = variant
                        spec_str = '{0}@{1} {2}'.format(
                            cls.name, version_str, variant_str
                        )

                        # Pop a few reserved keys from extra attributes, since
                        # they have a different semantics
                        external_path = extra_attributes.pop('prefix', None)
                        external_modules = extra_attributes.pop(
                            'modules', None
                        )
                        try:
                            spec = spack.spec.Spec(
                                spec_str,
                                external_path=external_path,
                                external_modules=external_modules
                            )
                        except Exception as e:
                            msg = 'Parsing failed [spec_str="{0}", error={1}]'
                            tty.debug(msg.format(spec_str, str(e)))
                        else:
                            specs.append(spack.spec.Spec.from_detection(
                                spec, extra_attributes=extra_attributes
                            ))

                return sorted(specs)

            @classmethod
            def determine_variants(cls, exes, version_str):
                return ''

            # Register the class as a detectable package
            detectable_packages[cls.namespace].append(cls.name)

            # Attach function implementations to the detectable class
            default = False
            if not hasattr(cls, 'determine_spec_details'):
                default = True
                cls.determine_spec_details = determine_spec_details

            if default and not hasattr(cls, 'determine_version'):
                msg = ('the package "{0}" in the "{1}" repo needs to define'
                       ' the "determine_version" method to be detectable')
                NotImplementedError(msg.format(cls.name, cls.namespace))

            if default and not hasattr(cls, 'determine_variants'):
                cls.determine_variants = determine_variants

        super(DetectablePackageMeta, cls).__init__(name, bases, attr_dict)


class PackageMeta(
    DetectablePackageMeta,
    spack.directives.DirectiveMeta,
    spack.mixins.PackageMixinsMeta,
    spack.multimethod.MultiMethodMeta
):
    """
    Package metaclass for supporting directives (e.g., depends_on) and phases
    """
    phase_fmt = '_InstallPhase_{0}'

    # These are accessed only through getattr, by name
    _InstallPhase_run_before = {}  # type: Dict[str, List[Callable]]
    _InstallPhase_run_after = {}  # type: Dict[str, List[Callable]]

    def __new__(cls, name, bases, attr_dict):
        """
        Instance creation is preceded by phase attribute transformations.

        Conveniently transforms attributes to permit extensible phases by
        iterating over the attribute 'phases' and creating / updating private
        InstallPhase attributes in the class that will be initialized in
        __init__.
        """
        if 'phases' in attr_dict:
            # Turn the strings in 'phases' into InstallPhase instances
            # and add them as private attributes
            _InstallPhase_phases = [PackageMeta.phase_fmt.format(x) for x in attr_dict['phases']]  # NOQA: ignore=E501
            for phase_name, callback_name in zip(_InstallPhase_phases, attr_dict['phases']):  # NOQA: ignore=E501
                attr_dict[phase_name] = InstallPhase(callback_name)
            attr_dict['_InstallPhase_phases'] = _InstallPhase_phases

        def _flush_callbacks(check_name):
            # Name of the attribute I am going to check it exists
            attr_name = PackageMeta.phase_fmt.format(check_name)
            checks = getattr(cls, attr_name)
            if checks:
                for phase_name, funcs in checks.items():
                    try:
                        # Search for the phase in the attribute dictionary
                        phase = attr_dict[
                            PackageMeta.phase_fmt.format(phase_name)]
                    except KeyError:
                        # If it is not there it's in the bases
                        # and we added a check. We need to copy
                        # and extend
                        for base in bases:
                            phase = getattr(
                                base,
                                PackageMeta.phase_fmt.format(phase_name),
                                None
                            )
                            if phase is not None:
                                break

                        attr_dict[PackageMeta.phase_fmt.format(
                            phase_name)] = phase.copy()
                        phase = attr_dict[
                            PackageMeta.phase_fmt.format(phase_name)]
                    getattr(phase, check_name).extend(funcs)
                # Clear the attribute for the next class
                setattr(cls, attr_name, {})

        _flush_callbacks('run_before')
        _flush_callbacks('run_after')

        # Reset names for packages that inherit from another
        # package with a different name
        attr_dict['_name'] = None

        return super(PackageMeta, cls).__new__(cls, name, bases, attr_dict)

    @staticmethod
    def register_callback(check_type, *phases):
        def _decorator(func):
            attr_name = PackageMeta.phase_fmt.format(check_type)
            check_list = getattr(PackageMeta, attr_name)
            for item in phases:
                checks = check_list.setdefault(item, [])
                checks.append(func)
            setattr(PackageMeta, attr_name, check_list)
            return func
        return _decorator

    @property
    def package_dir(self):
        """Directory where the package.py file lives."""
        return os.path.abspath(os.path.dirname(self.module.__file__))

    @property
    def module(self):
        """Module object (not just the name) that this package is defined in.

        We use this to add variables to package modules.  This makes
        install() methods easier to write (e.g., can call configure())
        """
        return __import__(self.__module__, fromlist=[self.__name__])

    @property
    def namespace(self):
        """Spack namespace for the package, which identifies its repo."""
        namespace, dot, module = self.__module__.rpartition('.')
        prefix = '%s.' % spack.repo.repo_namespace
        if namespace.startswith(prefix):
            namespace = namespace[len(prefix):]
        return namespace

    @property
    def fullname(self):
        """Name of this package, including the namespace"""
        return '%s.%s' % (self.namespace, self.name)

    @property
    def name(self):
        """The name of this package.

        The name of a package is the name of its Python module, without
        the containing module names.
        """
        if self._name is None:
            self._name = self.module.__name__
            if '.' in self._name:
                self._name = self._name[self._name.rindex('.') + 1:]
        return self._name


def run_before(*phases):
    """Registers a method of a package to be run before a given phase"""
    return PackageMeta.register_callback('run_before', *phases)


def run_after(*phases):
    """Registers a method of a package to be run after a given phase"""
    return PackageMeta.register_callback('run_after', *phases)


def on_package_attributes(**attr_dict):
    """Decorator: executes instance function only if object has attr valuses.

    Executes the decorated method only if at the moment of calling the
    instance has attributes that are equal to certain values.

    Args:
        attr_dict (dict): dictionary mapping attribute names to their
            required values
    """
    def _execute_under_condition(func):

        @functools.wraps(func)
        def _wrapper(instance, *args, **kwargs):
            # If all the attributes have the value we require, then execute
            has_all_attributes = all(
                [hasattr(instance, key) for key in attr_dict]
            )
            if has_all_attributes:
                has_the_right_values = all(
                    [getattr(instance, key) == value for key, value in attr_dict.items()]  # NOQA: ignore=E501
                )
                if has_the_right_values:
                    func(instance, *args, **kwargs)
        return _wrapper

    return _execute_under_condition


class PackageViewMixin(object):
    """This collects all functionality related to adding installed Spack
    package to views. Packages can customize how they are added to views by
    overriding these functions.
    """
    def view_source(self):
        """The source root directory that will be added to the view: files are
        added such that their path relative to the view destination matches
        their path relative to the view source.
        """
        return self.spec.prefix

    def view_destination(self, view):
        """The target root directory: each file is added relative to this
        directory.
        """
        return view.get_projection_for_spec(self.spec)

    def view_file_conflicts(self, view, merge_map):
        """Report any files which prevent adding this package to the view. The
        default implementation looks for any files which already exist.
        Alternative implementations may allow some of the files to exist in
        the view (in this case they would be omitted from the results).
        """
        return set(dst for dst in merge_map.values() if os.path.exists(dst))

    def add_files_to_view(self, view, merge_map):
        """Given a map of package files to destination paths in the view, add
        the files to the view. By default this adds all files. Alternative
        implementations may skip some files, for example if other packages
        linked into the view already include the file.
        """
        for src, dst in merge_map.items():
            if not os.path.exists(dst):
                view.link(src, dst, spec=self.spec)

    def remove_files_from_view(self, view, merge_map):
        """Given a map of package files to files currently linked in the view,
        remove the files from the view. The default implementation removes all
        files. Alternative implementations may not remove all files. For
        example if two packages include the same file, it should only be
        removed when both packages are removed.
        """
        for src, dst in merge_map.items():
            view.remove_file(src, dst)


def test_log_pathname(test_stage, spec):
    """Build the pathname of the test log file

    Args:
        test_stage (str): path to the test stage directory
        spec (Spec): instance of the spec under test

    Returns:
        (str): the pathname of the test log file
    """
    return os.path.join(test_stage,
                        'test-{0}-out.txt'.format(TestSuite.test_pkg_id(spec)))


class PackageBase(six.with_metaclass(PackageMeta, PackageViewMixin, object)):
    """This is the superclass for all spack packages.

    ***The Package class***

    At its core, a package consists of a set of software to be installed.
    A package may focus on a piece of software and its associated software
    dependencies or it may simply be a set, or bundle, of software.  The
    former requires defining how to fetch, verify (via, e.g., sha256), build,
    and install that software and the packages it depends on, so that
    dependencies can be installed along with the package itself.   The latter,
    sometimes referred to as a ``no-source`` package, requires only defining
    the packages to be built.

    Packages are written in pure Python.

    There are two main parts of a Spack package:

      1. **The package class**.  Classes contain ``directives``, which are
         special functions, that add metadata (versions, patches,
         dependencies, and other information) to packages (see
         ``directives.py``). Directives provide the constraints that are
         used as input to the concretizer.

      2. **Package instances**. Once instantiated, a package is
         essentially a software installer.  Spack calls methods like
         ``do_install()`` on the ``Package`` object, and it uses those to
         drive user-implemented methods like ``patch()``, ``install()``, and
         other build steps.  To install software, an instantiated package
         needs a *concrete* spec, which guides the behavior of the various
         install methods.

    Packages are imported from repos (see ``repo.py``).

    **Package DSL**

    Look in ``lib/spack/docs`` or check https://spack.readthedocs.io for
    the full documentation of the package domain-specific language.  That
    used to be partially documented here, but as it grew, the docs here
    became increasingly out of date.

    **Package Lifecycle**

    A package's lifecycle over a run of Spack looks something like this:

    .. code-block:: python

       p = Package()             # Done for you by spack

       p.do_fetch()              # downloads tarball from a URL (or VCS)
       p.do_stage()              # expands tarball in a temp directory
       p.do_patch()              # applies patches to expanded source
       p.do_install()            # calls package's install() function
       p.do_uninstall()          # removes install directory

    although packages that do not have code have nothing to fetch so omit
    ``p.do_fetch()``.

    There are also some other commands that clean the build area:

    .. code-block:: python

       p.do_clean()              # removes the stage directory entirely
       p.do_restage()            # removes the build directory and
                                 # re-expands the archive.

    The convention used here is that a ``do_*`` function is intended to be
    called internally by Spack commands (in ``spack.cmd``).  These aren't for
    package writers to override, and doing so may break the functionality
    of the Package class.

    Package creators have a lot of freedom, and they could technically
    override anything in this class.  That is not usually required.

    For most use cases.  Package creators typically just add attributes
    like ``homepage`` and, for a code-based package, ``url``, or functions
    such as ``install()``.
    There are many custom ``Package`` subclasses in the
    ``spack.build_systems`` package that make things even easier for
    specific build systems.

    """
    #
    # These are default values for instance variables.
    #

    #: A list or set of build time test functions to be called when tests
    #: are executed or 'None' if there are no such test functions.
    build_time_test_callbacks = None  # type: Optional[List[str]]

    #: By default, packages are not virtual
    #: Virtual packages override this attribute
    virtual = False

    #: Most Spack packages are used to install source or binary code while
    #: those that do not can be used to install a set of other Spack packages.
    has_code = True

    #: A list or set of install time test functions to be called when tests
    #: are executed or 'None' if there are no such test functions.
    install_time_test_callbacks = None  # type: Optional[List[str]]

    #: By default we build in parallel.  Subclasses can override this.
    parallel = True

    #: By default do not run tests within package's install()
    run_tests = False

    # FIXME: this is a bad object-oriented design, should be moved to Clang.
    #: By default do not setup mockup XCode on macOS with Clang
    use_xcode = False

    #: Most packages are NOT extendable. Set to True if you want extensions.
    extendable = False

    #: When True, add RPATHs for the entire DAG. When False, add RPATHs only
    #: for immediate dependencies.
    transitive_rpaths = True

    #: List of prefix-relative file paths (or a single path). If these do
    #: not exist after install, or if they exist but are not files,
    #: sanity checks fail.
    sanity_check_is_file = []  # type: List[str]

    #: List of prefix-relative directory paths (or a single path). If
    #: these do not exist after install, or if they exist but are not
    #: directories, sanity checks will fail.
    sanity_check_is_dir = []  # type: List[str]

    #: List of glob expressions. Each expression must either be
    #: absolute or relative to the package source path.
    #: Matching artifacts found at the end of the build process will be
    #: copied in the same directory tree as _spack_build_logfile and
    #: _spack_build_envfile.
    archive_files = []  # type: List[str]

    #: Boolean. Set to ``True`` for packages that require a manual download.
    #: This is currently used by package sanity tests and generation of a
    #: more meaningful fetch failure error.
    manual_download = False

    #: Set of additional options used when fetching package versions.
    fetch_options = {}  # type: Dict[str, Any]

    #
    # Set default licensing information
    #
    #: Boolean. If set to ``True``, this software requires a license.
    #: If set to ``False``, all of the ``license_*`` attributes will
    #: be ignored. Defaults to ``False``.
    license_required = False

    #: String. Contains the symbol used by the license manager to denote
    #: a comment. Defaults to ``#``.
    license_comment = '#'

    #: List of strings. These are files that the software searches for when
    #: looking for a license. All file paths must be relative to the
    #: installation directory. More complex packages like Intel may require
    #: multiple licenses for individual components. Defaults to the empty list.
    license_files = []  # type: List[str]

    #: List of strings. Environment variables that can be set to tell the
    #: software where to look for a license if it is not in the usual location.
    #: Defaults to the empty list.
    license_vars = []  # type: List[str]

    #: String. A URL pointing to license setup instructions for the software.
    #: Defaults to the empty string.
    license_url = ''

    #: Verbosity level, preserved across installs.
    _verbose = None

    #: index of patches by sha256 sum, built lazily
    _patches_by_hash = None

    #: Package homepage where users can find more information about the package
    homepage = None  # type: str

    #: Default list URL (place to find available versions)
    list_url = None  # type: str

    #: Link depth to which list_url should be searched for new versions
    list_depth = 0

    #: List of strings which contains GitHub usernames of package maintainers.
    #: Do not include @ here in order not to unnecessarily ping the users.
    maintainers = []  # type: List[str]

    #: List of attributes to be excluded from a package's hash.
    metadata_attrs = ['homepage', 'url', 'urls', 'list_url', 'extendable',
                      'parallel', 'make_jobs']

    #: Boolean. If set to ``True``, the smoke/install test requires a compiler.
    #: This is currently used by smoke tests to ensure a compiler is available
    #: to build a custom test code.
    test_requires_compiler = False

    #: List of test failures encountered during a smoke/install test run.
    test_failures = None

    #: TestSuite instance used to manage smoke/install tests for one or more
    #: specs.
    test_suite = None

    def __init__(self, spec):
        # this determines how the package should be built.
        self.spec = spec

        # Allow custom staging paths for packages
        self.path = None

        # Keep track of whether or not this package was installed from
        # a binary cache.
        self.installed_from_binary_cache = False

        # Ensure that only one of these two attributes are present
        if getattr(self, 'url', None) and getattr(self, 'urls', None):
            msg = "a package can have either a 'url' or a 'urls' attribute"
            msg += " [package '{0.name}' defines both]"
            raise ValueError(msg.format(self))

        # init internal variables
        self._stage = None
        self._fetcher = None

        # Set up timing variables
        self._fetch_time = 0.0
        self._total_time = 0.0

        if self.is_extension:
            spack.repo.get(self.extendee_spec)._check_extendable()

        super(PackageBase, self).__init__()

    @property
    def installed_upstream(self):
        if not hasattr(self, '_installed_upstream'):
            upstream, record = spack.store.db.query_by_spec_hash(
                self.spec.dag_hash())
            self._installed_upstream = upstream

        return self._installed_upstream

    @classmethod
    def possible_dependencies(
            cls, transitive=True, expand_virtuals=True, deptype='all',
            visited=None, missing=None, virtuals=None):
        """Return dict of possible dependencies of this package.

        Args:
            transitive (bool, optional): return all transitive dependencies if
                True, only direct dependencies if False (default True)..
            expand_virtuals (bool, optional): expand virtual dependencies into
                all possible implementations (default True)
            deptype (str or tuple, optional): dependency types to consider
            visited (dicct, optional): dict of names of dependencies visited so
                far, mapped to their immediate dependencies' names.
            missing (dict, optional): dict to populate with packages and their
                *missing* dependencies.
            virtuals (set): if provided, populate with virtuals seen so far.

        Returns:
            (dict): dictionary mapping dependency names to *their*
                immediate dependencies

        Each item in the returned dictionary maps a (potentially
        transitive) dependency of this package to its possible
        *immediate* dependencies. If ``expand_virtuals`` is ``False``,
        virtual package names wil be inserted as keys mapped to empty
        sets of dependencies.  Virtuals, if not expanded, are treated as
        though they have no immediate dependencies.

        Missing dependencies by default are ignored, but if a
        missing dict is provided, it will be populated with package names
        mapped to any dependencies they have that are in no
        repositories. This is only populated if transitive is True.

        Note: the returned dict *includes* the package itself.

        """
        deptype = spack.dependency.canonical_deptype(deptype)

        visited = {} if visited is None else visited
        missing = {} if missing is None else missing

        visited.setdefault(cls.name, set())

        for name, conditions in cls.dependencies.items():
            # check whether this dependency could be of the type asked for
            types = [dep.type for cond, dep in conditions.items()]
            types = set.union(*types)
            if not any(d in types for d in deptype):
                continue

            # expand virtuals if enabled, otherwise just stop at virtuals
            if spack.repo.path.is_virtual(name):
                if virtuals is not None:
                    virtuals.add(name)
                if expand_virtuals:
                    providers = spack.repo.path.providers_for(name)
                    dep_names = [spec.name for spec in providers]
                else:
                    visited.setdefault(cls.name, set()).add(name)
                    visited.setdefault(name, set())
                    continue
            else:
                dep_names = [name]

            # add the dependency names to the visited dict
            visited.setdefault(cls.name, set()).update(set(dep_names))

            # recursively traverse dependencies
            for dep_name in dep_names:
                if dep_name in visited:
                    continue

                visited.setdefault(dep_name, set())

                # skip the rest if not transitive
                if not transitive:
                    continue

                try:
                    dep_cls = spack.repo.path.get_pkg_class(dep_name)
                except spack.repo.UnknownPackageError:
                    # log unknown packages
                    missing.setdefault(cls.name, set()).add(dep_name)
                    continue

                dep_cls.possible_dependencies(
                    transitive, expand_virtuals, deptype, visited, missing,
                    virtuals)

        return visited

    def enum_constraints(self, visited=None):
        """Return transitive dependency constraints on this package."""
        if visited is None:
            visited = set()
        visited.add(self.name)

        names = []
        clauses = []

        for name in self.dependencies:
            if name not in visited and not spack.spec.Spec(name).virtual:
                pkg = spack.repo.get(name)
                dvis, dnames, dclauses = pkg.enum_constraints(visited)
                visited |= dvis
                names.extend(dnames)
                clauses.extend(dclauses)

        return visited

    # package_dir and module are *class* properties (see PackageMeta),
    # but to make them work on instances we need these defs as well.
    @property
    def package_dir(self):
        """Directory where the package.py file lives."""
        return type(self).package_dir

    @property
    def module(self):
        """Module object that this package is defined in."""
        return type(self).module

    @property
    def namespace(self):
        """Spack namespace for the package, which identifies its repo."""
        return type(self).namespace

    @property
    def fullname(self):
        """Name of this package, including namespace: namespace.name."""
        return type(self).fullname

    @property
    def name(self):
        """Name of this package (the module without parent modules)."""
        return type(self).name

    @property
    def global_license_dir(self):
        """Returns the directory where global license files for all
           packages are stored."""
        return os.path.join(spack.paths.prefix, 'etc', 'spack', 'licenses')

    @property
    def global_license_file(self):
        """Returns the path where a global license file for this
           particular package should be stored."""
        if not self.license_files:
            return
        return os.path.join(self.global_license_dir, self.name,
                            os.path.basename(self.license_files[0]))

    @property
    def version(self):
        if not self.spec.versions.concrete:
            raise ValueError("Version requested for a package that"
                             " does not have a concrete version.")
        return self.spec.versions[0]

    @memoized
    def version_urls(self):
        """OrderedDict of explicitly defined URLs for versions of this package.

        Return:
           An OrderedDict (version -> URL) different versions of this
           package, sorted by version.

        A version's URL only appears in the result if it has an an
        explicitly defined ``url`` argument. So, this list may be empty
        if a package only defines ``url`` at the top level.
        """
        version_urls = OrderedDict()
        for v, args in sorted(self.versions.items()):
            if 'url' in args:
                version_urls[v] = args['url']
        return version_urls

    def nearest_url(self, version):
        """Finds the URL with the "closest" version to ``version``.

        This uses the following precedence order:

          1. Find the next lowest or equal version with a URL.
          2. If no lower URL, return the next *higher* URL.
          3. If no higher URL, return None.

        """
        version_urls = self.version_urls()

        if version in version_urls:
            return version_urls[version]

        last_url = None
        for v, u in self.version_urls().items():
            if v > version:
                if last_url:
                    return last_url
            last_url = u

        return last_url

    def url_for_version(self, version):
        """Returns a URL from which the specified version of this package
        may be downloaded.

        version: class Version
            The version for which a URL is sought.

        See Class Version (version.py)
        """
        if not isinstance(version, Version):
            version = Version(version)

        # If we have a specific URL for this version, don't extrapolate.
        version_urls = self.version_urls()
        if version in version_urls:
            return version_urls[version]

        # If no specific URL, use the default, class-level URL
        url = getattr(self, 'url', None)
        urls = getattr(self, 'urls', [None])
        default_url = url or urls[0]

        # if no exact match AND no class-level default, use the nearest URL
        if not default_url:
            default_url = self.nearest_url(version)

            # if there are NO URLs to go by, then we can't do anything
            if not default_url:
                raise NoURLError(self.__class__)

        return spack.url.substitute_version(
            default_url, self.url_version(version))

    def _make_resource_stage(self, root_stage, fetcher, resource):
        resource_stage_folder = self._resource_stage(resource)
        mirror_paths = spack.mirror.mirror_archive_paths(
            fetcher,
            os.path.join(self.name, "%s-%s" % (resource.name, self.version)))
        stage = ResourceStage(resource.fetcher,
                              root=root_stage,
                              resource=resource,
                              name=resource_stage_folder,
                              mirror_paths=mirror_paths,
                              path=self.path)
        return stage

    def _download_search(self):
        dynamic_fetcher = fs.from_list_url(self)
        return [dynamic_fetcher] if dynamic_fetcher else []

    def _make_root_stage(self, fetcher):
        # Construct a mirror path (TODO: get this out of package.py)
        mirror_paths = spack.mirror.mirror_archive_paths(
            fetcher,
            os.path.join(self.name, "%s-%s" % (self.name, self.version)),
            self.spec)
        # Construct a path where the stage should build..
        s = self.spec
        stage_name = "{0}{1}-{2}-{3}".format(stage_prefix, s.name, s.version,
                                             s.dag_hash())

        stage = Stage(fetcher, mirror_paths=mirror_paths, name=stage_name,
                      path=self.path, search_fn=self._download_search)
        return stage

    def _make_stage(self):
        # If it's a dev package (not transitively), use a DIY stage object
        dev_path_var = self.spec.variants.get('dev_path', None)
        if dev_path_var:
            return spack.stage.DIYStage(dev_path_var.value)

        # Construct a composite stage on top of the composite FetchStrategy
        composite_fetcher = self.fetcher
        composite_stage = StageComposite()
        resources = self._get_needed_resources()
        for ii, fetcher in enumerate(composite_fetcher):
            if ii == 0:
                # Construct root stage first
                stage = self._make_root_stage(fetcher)
            else:
                # Construct resource stage
                resource = resources[ii - 1]  # ii == 0 is root!
                stage = self._make_resource_stage(composite_stage[0], fetcher,
                                                  resource)
            # Append the item to the composite
            composite_stage.append(stage)

        return composite_stage

    @property
    def stage(self):
        """Get the build staging area for this package.

        This automatically instantiates a ``Stage`` object if the package
        doesn't have one yet, but it does not create the Stage directory
        on the filesystem.
        """
        if not self.spec.versions.concrete:
            raise ValueError(
                "Cannot retrieve stage for package without concrete version.")
        if self._stage is None:
            self._stage = self._make_stage()
        return self._stage

    @stage.setter
    def stage(self, stage):
        """Allow a stage object to be set to override the default."""
        self._stage = stage

    @property
    def env_path(self):
        """Return the build environment file path associated with staging."""
        # Backward compatibility: Return the name of an existing log path;
        # otherwise, return the current install env path name.
        old_filename = os.path.join(self.stage.path, 'spack-build.env')
        if os.path.exists(old_filename):
            return old_filename
        else:
            return os.path.join(self.stage.path, _spack_build_envfile)

    @property
    def metadata_dir(self):
        """Return the install metadata directory."""
        return spack.store.layout.metadata_path(self.spec)

    @property
    def install_env_path(self):
        """
        Return the build environment file path on successful installation.
        """
        # Backward compatibility: Return the name of an existing log path;
        # otherwise, return the current install env path name.
        old_filename = os.path.join(self.metadata_dir, 'build.env')
        if os.path.exists(old_filename):
            return old_filename
        else:
            return os.path.join(self.metadata_dir, _spack_build_envfile)

    @property
    def log_path(self):
        """Return the build log file path associated with staging."""
        # Backward compatibility: Return the name of an existing log path.
        for filename in ['spack-build.out', 'spack-build.txt']:
            old_log = os.path.join(self.stage.path, filename)
            if os.path.exists(old_log):
                return old_log

        # Otherwise, return the current log path name.
        return os.path.join(self.stage.path, _spack_build_logfile)

    @property
    def install_log_path(self):
        """Return the build log file path on successful installation."""
        # Backward compatibility: Return the name of an existing install log.
        for filename in ['build.out', 'build.txt']:
            old_log = os.path.join(self.metadata_dir, filename)
            if os.path.exists(old_log):
                return old_log

        # Otherwise, return the current install log path name.
        return os.path.join(self.metadata_dir, _spack_build_logfile)

    @property
    def configure_args_path(self):
        """Return the configure args file path associated with staging."""
        return os.path.join(self.stage.path, _spack_configure_argsfile)

    @property
    def install_configure_args_path(self):
        """Return the configure args file path on successful installation."""
        return os.path.join(self.metadata_dir, _spack_configure_argsfile)

    @property
    def install_test_root(self):
        """Return the install test root directory."""
        return os.path.join(self.metadata_dir, 'test')

    def _make_fetcher(self):
        # Construct a composite fetcher that always contains at least
        # one element (the root package). In case there are resources
        # associated with the package, append their fetcher to the
        # composite.
        root_fetcher = fs.for_package_version(self, self.version)
        fetcher = fs.FetchStrategyComposite()  # Composite fetcher
        fetcher.append(root_fetcher)  # Root fetcher is always present
        resources = self._get_needed_resources()
        for resource in resources:
            fetcher.append(resource.fetcher)
        return fetcher

    @property
    def fetcher(self):
        if not self.spec.versions.concrete:
            raise ValueError("Cannot retrieve fetcher for"
                             " package without concrete version.")
        if not self._fetcher:
            self._fetcher = self._make_fetcher()
        return self._fetcher

    @fetcher.setter
    def fetcher(self, f):
        self._fetcher = f

    def dependencies_of_type(self, *deptypes):
        """Get dependencies that can possibly have these deptypes.

        This analyzes the package and determines which dependencies *can*
        be a certain kind of dependency. Note that they may not *always*
        be this kind of dependency, since dependencies can be optional,
        so something may be a build dependency in one configuration and a
        run dependency in another.
        """
        return dict(
            (name, conds) for name, conds in self.dependencies.items()
            if any(dt in self.dependencies[name][cond].type
                   for cond in conds for dt in deptypes))

    @property
    def extendee_spec(self):
        """
        Spec of the extendee of this package, or None if it is not an extension
        """
        if not self.extendees:
            return None

        # TODO: allow more than one extendee.
        name = next(iter(self.extendees))

        # If the extendee is in the spec's deps already, return that.
        for dep in self.spec.traverse(deptypes=('link', 'run')):
            if name == dep.name:
                return dep

        # if the spec is concrete already, then it extends something
        # that is an *optional* dependency, and the dep isn't there.
        if self.spec._concrete:
            return None
        else:
            # If it's not concrete, then return the spec from the
            # extends() directive since that is all we know so far.
            spec, kwargs = self.extendees[name]
            return spec

    @property
    def extendee_args(self):
        """
        Spec of the extendee of this package, or None if it is not an extension
        """
        if not self.extendees:
            return None

        # TODO: allow multiple extendees.
        name = next(iter(self.extendees))
        return self.extendees[name][1]

    @property
    def is_extension(self):
        # if it is concrete, it's only an extension if it actually
        # dependes on the extendee.
        if self.spec._concrete:
            return self.extendee_spec is not None
        else:
            # If not, then it's an extension if it *could* be an extension
            return bool(self.extendees)

    def extends(self, spec):
        '''
        Returns True if this package extends the given spec.

        If ``self.spec`` is concrete, this returns whether this package extends
        the given spec.

        If ``self.spec`` is not concrete, this returns whether this package may
        extend the given spec.
        '''
        if spec.name not in self.extendees:
            return False
        s = self.extendee_spec
        return s and spec.satisfies(s)

    def is_activated(self, view):
        """Return True if package is activated."""
        if not self.is_extension:
            raise ValueError(
                "is_activated called on package that is not an extension.")
        if self.extendee_spec.package.installed_upstream:
            # If this extends an upstream package, it cannot be activated for
            # it. This bypasses construction of the extension map, which can
            # can fail when run in the context of a downstream Spack instance
            return False
        extensions_layout = view.extensions_layout
        exts = extensions_layout.extension_map(self.extendee_spec)
        return (self.name in exts) and (exts[self.name] == self.spec)

    def provides(self, vpkg_name):
        """
        True if this package provides a virtual package with the specified name
        """
        return any(
            any(self.spec.satisfies(c) for c in constraints)
            for s, constraints in self.provided.items() if s.name == vpkg_name
        )

    @property
    def virtuals_provided(self):
        """
        virtual packages provided by this package with its spec
        """
        return [vspec for vspec, constraints in self.provided.items()
                if any(self.spec.satisfies(c) for c in constraints)]

    @property
    def installed(self):
        """Installation status of a package.

        Returns:
            True if the package has been installed, False otherwise.
        """
        has_prefix = os.path.isdir(self.prefix)
        try:
            # If the spec is in the DB, check the installed
            # attribute of the record
            rec = spack.store.db.get_record(self.spec)
            db_says_installed = rec.installed
        except KeyError:
            # If the spec is not in the DB, the method
            #  above raises a Key error
            db_says_installed = False

        return has_prefix and db_says_installed

    @property
    def prefix(self):
        """Get the prefix into which this package should be installed."""
        return self.spec.prefix

    @property
    def architecture(self):
        """Get the spack.architecture.Arch object that represents the
        environment in which this package will be built."""
        if not self.spec.concrete:
            raise ValueError("Can only get the arch for concrete package.")
        return spack.architecture.arch_for_spec(self.spec.architecture)

    @property
    def compiler(self):
        """Get the spack.compiler.Compiler object used to build this package"""
        if not self.spec.concrete:
            raise ValueError("Can only get a compiler for a concrete package.")
        return spack.compilers.compiler_for_spec(self.spec.compiler,
                                                 self.spec.architecture)

    def url_version(self, version):
        """
        Given a version, this returns a string that should be substituted
        into the package's URL to download that version.

        By default, this just returns the version string. Subclasses may need
        to override this, e.g. for boost versions where you need to ensure that
        there are _'s in the download URL.
        """
        return str(version)

    def remove_prefix(self):
        """
        Removes the prefix for a package along with any empty parent
        directories
        """
        spack.store.layout.remove_install_directory(self.spec)

    @property
    def download_instr(self):
        """
        Defines the default manual download instructions.  Packages can
        override the property to provide more information.

        Returns:
            (str):  default manual download instructions
        """
        required = ('Manual download is required for {0}. '
                    .format(self.spec.name) if self.manual_download else '')
        return ('{0}Refer to {1} for download instructions.'
                .format(required, self.spec.package.homepage))

    def do_fetch(self, mirror_only=False):
        """
        Creates a stage directory and downloads the tarball for this package.
        Working directory will be set to the stage directory.
        """
        if not self.has_code:
            tty.debug('No fetch required for {0}: package has no code.'
                      .format(self.name))

        checksum = spack.config.get('config:checksum')
        fetch = self.stage.managed_by_spack
        if checksum and fetch and self.version not in self.versions:
            tty.warn("There is no checksum on file to fetch %s safely." %
                     self.spec.cformat('{name}{@version}'))

            # Ask the user whether to skip the checksum if we're
            # interactive, but just fail if non-interactive.
            ck_msg = "Add a checksum or use --no-checksum to skip this check."
            ignore_checksum = False
            if sys.stdout.isatty():
                ignore_checksum = tty.get_yes_or_no("  Fetch anyway?",
                                                    default=False)
                if ignore_checksum:
                    tty.debug('Fetching with no checksum. {0}'
                              .format(ck_msg))

            if not ignore_checksum:
                raise FetchError("Will not fetch %s" %
                                 self.spec.format('{name}{@version}'), ck_msg)

        deprecated = spack.config.get('config:deprecated')
        if not deprecated and self.versions.get(
                self.version, {}).get('deprecated', False):
            tty.warn("{0} is deprecated and may be removed in a future Spack "
                     "release.".format(
                         self.spec.format('{name}{@version}')))

            # Ask the user whether to install deprecated version if we're
            # interactive, but just fail if non-interactive.
            dp_msg = ("If you are willing to be a maintainer for this version "
                      "of the package, submit a PR to remove `deprecated=False"
                      "`, or use `--deprecated` to skip this check.")
            ignore_deprecation = False
            if sys.stdout.isatty():
                ignore_deprecation = tty.get_yes_or_no("  Fetch anyway?",
                                                       default=False)

                if ignore_deprecation:
                    tty.debug("Fetching deprecated version. {0}".format(
                        dp_msg))

            if not ignore_deprecation:
                raise FetchError("Will not fetch {0}".format(
                    self.spec.format('{name}{@version}')), dp_msg)

        self.stage.create()
        err_msg = None if not self.manual_download else self.download_instr
        start_time = time.time()
        self.stage.fetch(mirror_only, err_msg=err_msg)
        self._fetch_time = time.time() - start_time

        if checksum and self.version in self.versions:
            self.stage.check()

        self.stage.cache_local()

        for patch in self.spec.patches:
            patch.fetch()
            if patch.stage:
                patch.stage.cache_local()

    def do_stage(self, mirror_only=False):
        """Unpacks and expands the fetched tarball."""
        # Always create the stage directory at this point.  Why?  A no-code
        # package may want to use the installation process to install metadata.
        self.stage.create()

        # Fetch/expand any associated code.
        if self.has_code:
            self.do_fetch(mirror_only)
            self.stage.expand_archive()

            if not os.listdir(self.stage.path):
                raise FetchError("Archive was empty for %s" % self.name)
        else:
            # Support for post-install hooks requires a stage.source_path
            fsys.mkdirp(self.stage.source_path)

    def do_patch(self):
        """Applies patches if they haven't been applied already."""
        if not self.spec.concrete:
            raise ValueError("Can only patch concrete packages.")

        # Kick off the stage first.  This creates the stage.
        self.do_stage()

        # Package can add its own patch function.
        has_patch_fun = hasattr(self, 'patch') and callable(self.patch)

        # Get the patches from the spec (this is a shortcut for the MV-variant)
        patches = self.spec.patches

        # If there are no patches, note it.
        if not patches and not has_patch_fun:
            tty.msg('No patches needed for {0}'.format(self.name))
            return

        # Construct paths to special files in the archive dir used to
        # keep track of whether patches were successfully applied.
        archive_dir = self.stage.source_path
        good_file = os.path.join(archive_dir, '.spack_patched')
        no_patches_file = os.path.join(archive_dir, '.spack_no_patches')
        bad_file = os.path.join(archive_dir, '.spack_patch_failed')

        # If we encounter an archive that failed to patch, restage it
        # so that we can apply all the patches again.
        if os.path.isfile(bad_file):
            tty.debug('Patching failed last time. Restaging.')
            self.stage.restage()

        # If this file exists, then we already applied all the patches.
        if os.path.isfile(good_file):
            tty.msg('Already patched {0}'.format(self.name))
            return
        elif os.path.isfile(no_patches_file):
            tty.msg('No patches needed for {0}'.format(self.name))
            return

        # Apply all the patches for specs that match this one
        patched = False
        for patch in patches:
            try:
                with fsys.working_dir(self.stage.source_path):
                    patch.apply(self.stage)
                tty.msg('Applied patch {0}'.format(patch.path_or_url))
                patched = True
            except spack.error.SpackError as e:
                tty.debug(e)

                # Touch bad file if anything goes wrong.
                tty.msg('Patch %s failed.' % patch.path_or_url)
                fsys.touch(bad_file)
                raise

        if has_patch_fun:
            try:
                with fsys.working_dir(self.stage.source_path):
                    self.patch()
                tty.msg('Ran patch() for {0}'.format(self.name))
                patched = True
            except spack.multimethod.NoSuchMethodError:
                # We are running a multimethod without a default case.
                # If there's no default it means we don't need to patch.
                if not patched:
                    # if we didn't apply a patch from a patch()
                    # directive, AND the patch function didn't apply, say
                    # no patches are needed.  Otherwise, we already
                    # printed a message for each patch.
                    tty.msg('No patches needed for {0}'.format(self.name))
            except spack.error.SpackError as e:
                tty.debug(e)

                # Touch bad file if anything goes wrong.
                tty.msg('patch() function failed for {0}'.format(self.name))
                fsys.touch(bad_file)
                raise

        # Get rid of any old failed file -- patches have either succeeded
        # or are not needed.  This is mostly defensive -- it's needed
        # if the restage() method doesn't clean *everything* (e.g., for a repo)
        if os.path.isfile(bad_file):
            os.remove(bad_file)

        # touch good or no patches file so that we skip next time.
        if patched:
            fsys.touch(good_file)
        else:
            fsys.touch(no_patches_file)

    @classmethod
    def all_patches(cls):
        """Retrieve all patches associated with the package.

        Retrieves patches on the package itself as well as patches on the
        dependencies of the package."""
        patches = []
        for _, patch_list in cls.patches.items():
            for patch in patch_list:
                patches.append(patch)

        pkg_deps = cls.dependencies
        for dep_name in pkg_deps:
            for _, dependency in pkg_deps[dep_name].items():
                for _, patch_list in dependency.patches.items():
                    for patch in patch_list:
                        patches.append(patch)

        return patches

    def content_hash(self, content=None):
        """Create a hash based on the sources and logic used to build the
        package. This includes the contents of all applied patches and the
        contents of applicable functions in the package subclass."""
        if not self.spec.concrete:
            err_msg = ("Cannot invoke content_hash on a package"
                       " if the associated spec is not concrete")
            raise spack.error.SpackError(err_msg)

        hash_content = list()
        try:
            source_id = fs.for_package_version(self, self.version).source_id()
        except fs.ExtrapolationError:
            source_id = None
        if not source_id:
            # TODO? in cases where a digest or source_id isn't available,
            # should this attempt to download the source and set one? This
            # probably only happens for source repositories which are
            # referenced by branch name rather than tag or commit ID.
            message = 'Missing a source id for {s.name}@{s.version}'
            tty.warn(message.format(s=self))
            hash_content.append(''.encode('utf-8'))
        else:
            hash_content.append(source_id.encode('utf-8'))
        hash_content.extend(':'.join((p.sha256, str(p.level))).encode('utf-8')
                            for p in self.spec.patches)
        hash_content.append(package_hash(self.spec, content))
        b32_hash = base64.b32encode(
            hashlib.sha256(bytes().join(
                sorted(hash_content))).digest()).lower()

        # convert from bytes if running python 3
        if sys.version_info[0] >= 3:
            b32_hash = b32_hash.decode('utf-8')

        return b32_hash

    def _has_make_target(self, target):
        """Checks to see if 'target' is a valid target in a Makefile.

        Parameters:
            target (str): the target to check for

        Returns:
            bool: True if 'target' is found, else False
        """
        # Prevent altering LC_ALL for 'make' outside this function
        make = copy.deepcopy(inspect.getmodule(self).make)

        # Use English locale for missing target message comparison
        make.add_default_env('LC_ALL', 'C')

        # Check if we have a Makefile
        for makefile in ['GNUmakefile', 'Makefile', 'makefile']:
            if os.path.exists(makefile):
                break
        else:
            tty.debug('No Makefile found in the build directory')
            return False

        # Check if 'target' is a valid target.
        #
        # `make -n target` performs a "dry run". It prints the commands that
        # would be run but doesn't actually run them. If the target does not
        # exist, you will see one of the following error messages:
        #
        # GNU Make:
        #     make: *** No rule to make target `test'.  Stop.
        #           *** No rule to make target 'test'.  Stop.
        #
        # BSD Make:
        #     make: don't know how to make test. Stop
        missing_target_msgs = [
            "No rule to make target `{0}'.  Stop.",
            "No rule to make target '{0}'.  Stop.",
            "don't know how to make {0}. Stop",
        ]

        kwargs = {
            'fail_on_error': False,
            'output': os.devnull,
            'error': str,
        }

        stderr = make('-n', target, **kwargs)

        for missing_target_msg in missing_target_msgs:
            if missing_target_msg.format(target) in stderr:
                tty.debug("Target '{0}' not found in {1}"
                          .format(target, makefile))
                return False

        return True

    def _if_make_target_execute(self, target, *args, **kwargs):
        """Runs ``make target`` if 'target' is a valid target in the Makefile.

        Parameters:
            target (str): the target to potentially execute
        """
        if self._has_make_target(target):
            # Execute target
            inspect.getmodule(self).make(target, *args, **kwargs)

    def _has_ninja_target(self, target):
        """Checks to see if 'target' is a valid target in a Ninja build script.

        Parameters:
            target (str): the target to check for

        Returns:
            bool: True if 'target' is found, else False
        """
        ninja = inspect.getmodule(self).ninja

        # Check if we have a Ninja build script
        if not os.path.exists('build.ninja'):
            tty.debug('No Ninja build script found in the build directory')
            return False

        # Get a list of all targets in the Ninja build script
        # https://ninja-build.org/manual.html#_extra_tools
        all_targets = ninja('-t', 'targets', 'all', output=str).split('\n')

        # Check if 'target' is a valid target
        matches = [line for line in all_targets
                   if line.startswith(target + ':')]

        if not matches:
            tty.debug("Target '{0}' not found in build.ninja"
                      .format(target))
            return False

        return True

    def _if_ninja_target_execute(self, target, *args, **kwargs):
        """Runs ``ninja target`` if 'target' is a valid target in the Ninja
        build script.

        Parameters:
            target (str): the target to potentially execute
        """
        if self._has_ninja_target(target):
            # Execute target
            inspect.getmodule(self).ninja(target, *args, **kwargs)

    def _get_needed_resources(self):
        resources = []
        # Select the resources that are needed for this build
        if self.spec.concrete:
            for when_spec, resource_list in self.resources.items():
                if when_spec in self.spec:
                    resources.extend(resource_list)
        else:
            for when_spec, resource_list in self.resources.items():
                # Note that variant checking is always strict for specs where
                # the name is not specified. But with strict variant checking,
                # only variants mentioned in 'other' are checked. Here we only
                # want to make sure that no constraints in when_spec
                # conflict with the spec, so we need to invoke
                # when_spec.satisfies(self.spec) vs.
                # self.spec.satisfies(when_spec)
                if when_spec.satisfies(self.spec, strict=False):
                    resources.extend(resource_list)
        # Sorts the resources by the length of the string representing their
        # destination. Since any nested resource must contain another
        # resource's name in its path, it seems that should work
        resources = sorted(resources, key=lambda res: len(res.destination))
        return resources

    def _resource_stage(self, resource):
        pieces = ['resource', resource.name, self.spec.dag_hash()]
        resource_stage_folder = '-'.join(pieces)
        return resource_stage_folder

    @contextlib.contextmanager
    def _stage_and_write_lock(self):
        """Prefix lock nested in a stage."""
        with self.stage:
            with spack.store.db.prefix_write_lock(self.spec):
                yield

    def do_install(self, **kwargs):
        """Called by commands to install a package and or its dependencies.

        Package implementations should override install() to describe
        their build process.

        Args:
            cache_only (bool): Fail if binary package unavailable.
            dirty (bool): Don't clean the build environment before installing.
            explicit (bool): True if package was explicitly installed, False
                if package was implicitly installed (as a dependency).
            fail_fast (bool): Fail if any dependency fails to install;
                otherwise, the default is to install as many dependencies as
                possible (i.e., best effort installation).
            fake (bool): Don't really build; install fake stub files instead.
            force (bool): Install again, even if already installed.
            install_deps (bool): Install dependencies before installing this
                package
            install_source (bool): By default, source is not installed, but
                for debugging it might be useful to keep it around.
            keep_prefix (bool): Keep install prefix on failure. By default,
                destroys it.
            keep_stage (bool): By default, stage is destroyed only if there
                are no exceptions during build. Set to True to keep the stage
                even with exceptions.
            restage (bool): Force spack to restage the package source.
            skip_patch (bool): Skip patch stage of build if True.
            stop_before (InstallPhase): stop execution before this
                installation phase (or None)
            stop_at (InstallPhase): last installation phase to be executed
                (or None)
            tests (bool or list or set): False to run no tests, True to test
                all packages, or a list of package names to run tests for some
            use_cache (bool): Install from binary package, if available.
            verbose (bool): Display verbose build output (by default,
                suppresses it)
        """
        # Non-transitive dev specs need to keep the dev stage and be built from
        # source every time. Transitive ones just need to be built from source.
        dev_path_var = self.spec.variants.get('dev_path', None)
        if dev_path_var:
            kwargs['keep_stage'] = True

        builder = PackageInstaller([(self, kwargs)])
        builder.install()

    def cache_extra_test_sources(self, srcs):
        """Copy relative source paths to the corresponding install test subdir

        This method is intended as an optional install test setup helper for
        grabbing source files/directories during the installation process and
        copying them to the installation test subdirectory for subsequent use
        during install testing.

        Args:
            srcs (str or list of str): relative path for files and or
                subdirectories located in the staged source path that are to
                be copied to the corresponding location(s) under the install
                testing directory.
        """
        paths = [srcs] if isinstance(srcs, six.string_types) else srcs

        for path in paths:
            src_path = os.path.join(self.stage.source_path, path)
            dest_path = os.path.join(self.install_test_root, path)
            if os.path.isdir(src_path):
                fsys.install_tree(src_path, dest_path)
            else:
                fsys.mkdirp(os.path.dirname(dest_path))
                fsys.copy(src_path, dest_path)

    def do_test(self, dirty=False):
        if self.test_requires_compiler:
            compilers = spack.compilers.compilers_for_spec(
                self.spec.compiler, arch_spec=self.spec.architecture)
            if not compilers:
                tty.error('Skipping tests for package %s\n' %
                          self.spec.format('{name}-{version}-{hash:7}') +
                          'Package test requires missing compiler %s' %
                          self.spec.compiler)
                return

        # Clear test failures
        self.test_failures = []
        self.test_log_file = self.test_suite.log_file_for_spec(self.spec)
        fsys.touch(self.test_log_file)  # Otherwise log_parse complains

        kwargs = {'dirty': dirty, 'fake': False, 'context': 'test'}
        spack.build_environment.start_build_process(self, test_process, kwargs)

    def test(self):
        pass

    def run_test(self, exe, options=[], expected=[], status=0,
                 installed=False, purpose='', skip_missing=False,
                 work_dir=None):
        """Run the test and confirm the expected results are obtained

        Log any failures and continue, they will be re-raised later

        Args:
            exe (str): the name of the executable
            options (str or list of str): list of options to pass to the runner
            expected (str or list of str): list of expected output strings.
                Each string is a regex expected to match part of the output.
            status (int or list of int): possible passing status values
                with 0 meaning the test is expected to succeed
            installed (bool): if ``True``, the executable must be in the
                install prefix
            purpose (str): message to display before running test
            skip_missing (bool): skip the test if the executable is not
                in the install prefix bin directory or the provided work_dir
            work_dir (str or None): path to the smoke test directory
        """
        wdir = '.' if work_dir is None else work_dir
        with fsys.working_dir(wdir, create=True):
            try:
                runner = which(exe)
                if runner is None and skip_missing:
                    return
                assert runner is not None, \
                    "Failed to find executable '{0}'".format(exe)

                self._run_test_helper(
                    runner, options, expected, status, installed, purpose)
                print("PASSED")
                return True
            except BaseException as e:
                # print a summary of the error to the log file
                # so that cdash and junit reporters know about it
                exc_type, _, tb = sys.exc_info()
                print('FAILED: {0}'.format(e))
                import traceback
                # remove the current call frame to exclude the extract_stack
                # call from the error
                stack = traceback.extract_stack()[:-1]

                # Package files have a line added at import time, so we re-read
                # the file to make line numbers match. We have to subtract two
                # from the line number because the original line number is
                # inflated once by the import statement and the lines are
                # displaced one by the import statement.
                for i, entry in enumerate(stack):
                    filename, lineno, function, text = entry
                    if spack.repo.is_package_file(filename):
                        with open(filename, 'r') as f:
                            lines = f.readlines()
                        new_lineno = lineno - 2
                        text = lines[new_lineno]
                        stack[i] = (filename, new_lineno, function, text)

                # Format the stack to print and print it
                out = traceback.format_list(stack)
                for line in out:
                    print(line.rstrip('\n'))

                if exc_type is spack.util.executable.ProcessError:
                    out = six.StringIO()
                    spack.build_environment.write_log_summary(
                        out, 'test', self.test_log_file, last=1)
                    m = out.getvalue()
                else:
                    # We're below the package context, so get context from
                    # stack instead of from traceback.
                    # The traceback is truncated here, so we can't use it to
                    # traverse the stack.
                    m = '\n'.join(
                        spack.build_environment.get_package_context(tb)
                    )

                exc = e  # e is deleted after this block

                # If we fail fast, raise another error
                if spack.config.get('config:fail_fast', False):
                    raise TestFailure([(exc, m)])
                else:
                    self.test_failures.append((exc, m))
                return False

    def _run_test_helper(self, runner, options, expected, status, installed,
                         purpose):
        status = [status] if isinstance(status, six.integer_types) else status
        expected = [expected] if isinstance(expected, six.string_types) else \
            expected
        options = [options] if isinstance(options, six.string_types) else \
            options

        if purpose:
            tty.msg(purpose)
        else:
            tty.debug('test: {0}: expect command status in {1}'
                      .format(runner.name, status))

        if installed:
            msg = "Executable '{0}' expected in prefix".format(runner.name)
            msg += ", found in {0} instead".format(runner.path)
            assert runner.path.startswith(self.spec.prefix), msg

        try:
            output = runner(*options, output=str.split, error=str.split)

            assert 0 in status, \
                'Expected {0} execution to fail'.format(runner.name)
        except ProcessError as err:
            output = str(err)
            match = re.search(r'exited with status ([0-9]+)', output)
            if not (match and int(match.group(1)) in status):
                raise

        for check in expected:
            cmd = ' '.join([runner.name] + options)
            msg = "Expected '{0}' to match output of `{1}`".format(check, cmd)
            msg += '\n\nOutput: {0}'.format(output)
            assert re.search(check, output), msg

    def unit_test_check(self):
        """Hook for unit tests to assert things about package internals.

        Unit tests can override this function to perform checks after
        ``Package.install`` and all post-install hooks run, but before
        the database is updated.

        The overridden function may indicate that the install procedure
        should terminate early (before updating the database) by
        returning ``False`` (or any value such that ``bool(result)`` is
        ``False``).

        Return:
            (bool): ``True`` to continue, ``False`` to skip ``install()``
        """
        return True

    def sanity_check_prefix(self):
        """This function checks whether install succeeded."""

        def check_paths(path_list, filetype, predicate):
            if isinstance(path_list, six.string_types):
                path_list = [path_list]

            for path in path_list:
                abs_path = os.path.join(self.prefix, path)
                if not predicate(abs_path):
                    raise InstallError(
                        "Install failed for %s. No such %s in prefix: %s" %
                        (self.name, filetype, path))

        check_paths(self.sanity_check_is_file, 'file', os.path.isfile)
        check_paths(self.sanity_check_is_dir, 'directory', os.path.isdir)

        installed = set(os.listdir(self.prefix))
        installed.difference_update(
            spack.store.layout.hidden_file_paths)
        if not installed:
            raise InstallError(
                "Install failed for %s.  Nothing was installed!" % self.name)

    @property
    def build_log_path(self):
        """
        Return the expected (or current) build log file path.  The path points
        to the staging build file until the software is successfully installed,
        when it points to the file in the installation directory.
        """
        return self.install_log_path if self.installed else self.log_path

    @classmethod
    def inject_flags(cls, name, flags):
        """
        flag_handler that injects all flags through the compiler wrapper.
        """
        return (flags, None, None)

    @classmethod
    def env_flags(cls, name, flags):
        """
        flag_handler that adds all flags to canonical environment variables.
        """
        return (None, flags, None)

    @classmethod
    def build_system_flags(cls, name, flags):
        """
        flag_handler that passes flags to the build system arguments.  Any
        package using `build_system_flags` must also implement
        `flags_to_build_system_args`, or derive from a class that
        implements it.  Currently, AutotoolsPackage and CMakePackage
        implement it.
        """
        return (None, None, flags)

    def _get_legacy_environment_method(self, method_name):
        legacy_fn = getattr(self, method_name, None)
        name_prefix = method_name.split('_environment')[0]
        if legacy_fn:
            msg = '[DEPRECATED METHOD]\n"{0}" ' \
                  'still defines the deprecated method "{1}" ' \
                  '[should be split into "{2}_build_environment" and ' \
                  '"{2}_run_environment"]'
            tty.debug(msg.format(self.name, method_name, name_prefix))
        return legacy_fn

    def setup_build_environment(self, env):
        """Sets up the build environment for a package.

        This method will be called before the current package prefix exists in
        Spack's store.

        Args:
            env (EnvironmentModifications): environment modifications to be
                applied when the package is built. Package authors can call
                methods on it to alter the build environment.
        """
        legacy_fn = self._get_legacy_environment_method('setup_environment')
        if legacy_fn:
            _ = spack.util.environment.EnvironmentModifications()
            legacy_fn(env, _)

    def setup_run_environment(self, env):
        """Sets up the run environment for a package.

        Args:
            env (EnvironmentModifications): environment modifications to be
                applied when the package is run. Package authors can call
                methods on it to alter the run environment.
        """
        legacy_fn = self._get_legacy_environment_method('setup_environment')
        if legacy_fn:
            _ = spack.util.environment.EnvironmentModifications()
            legacy_fn(_, env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Sets up the build environment of packages that depend on this one.

        This is similar to ``setup_build_environment``, but it is used to
        modify the build environments of packages that *depend* on this one.

        This gives packages like Python and others that follow the extension
        model a way to implement common environment or compile-time settings
        for dependencies.

        This method will be called before the dependent package prefix exists
        in Spack's store.

        Examples:
            1. Installing python modules generally requires ``PYTHONPATH``
            to point to the ``lib/pythonX.Y/site-packages`` directory in the
            module's install prefix. This method could be used to set that
            variable.

        Args:
            env (EnvironmentModifications): environment modifications to be
                applied when the dependent package is built. Package authors
                can call methods on it to alter the build environment.

            dependent_spec (Spec): the spec of the dependent package
                about to be built. This allows the extendee (self) to query
                the dependent's state. Note that *this* package's spec is
                available as ``self.spec``
        """
        legacy_fn = self._get_legacy_environment_method(
            'setup_dependent_environment'
        )
        if legacy_fn:
            _ = spack.util.environment.EnvironmentModifications()
            legacy_fn(env, _, dependent_spec)

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Sets up the run environment of packages that depend on this one.

        This is similar to ``setup_run_environment``, but it is used to
        modify the run environments of packages that *depend* on this one.

        This gives packages like Python and others that follow the extension
        model a way to implement common environment or run-time settings
        for dependencies.

        Args:
            env (EnvironmentModifications): environment modifications to be
                applied when the dependent package is run. Package authors
                can call methods on it to alter the build environment.

            dependent_spec (Spec): The spec of the dependent package
                about to be run. This allows the extendee (self) to query
                the dependent's state. Note that *this* package's spec is
                available as ``self.spec``
        """
        legacy_fn = self._get_legacy_environment_method(
            'setup_dependent_environment'
        )
        if legacy_fn:
            _ = spack.util.environment.EnvironmentModifications()
            legacy_fn(_, env, dependent_spec)

    def setup_dependent_package(self, module, dependent_spec):
        """Set up Python module-scope variables for dependent packages.

        Called before the install() method of dependents.

        Default implementation does nothing, but this can be
        overridden by an extendable package to set up the module of
        its extensions. This is useful if there are some common steps
        to installing all extensions for a certain package.

        Examples:

        1. Extensions often need to invoke the ``python`` interpreter
           from the Python installation being extended. This routine
           can put a ``python()`` Executable object in the module scope
           for the extension package to simplify extension installs.

        2. MPI compilers could set some variables in the dependent's
           scope that point to ``mpicc``, ``mpicxx``, etc., allowing
           them to be called by common name regardless of which MPI is used.

        3. BLAS/LAPACK implementations can set some variables
           indicating the path to their libraries, since these
           paths differ by BLAS/LAPACK implementation.

        Args:
            module (spack.package.PackageBase.module): The Python ``module``
                object of the dependent package. Packages can use this to set
                module-scope variables for the dependent to use.

            dependent_spec (Spec): The spec of the dependent package
                about to be built. This allows the extendee (self) to
                query the dependent's state.  Note that *this*
                package's spec is available as ``self.spec``.
        """
        pass

    flag_handler = inject_flags
    # The flag handler method is called for each of the allowed compiler flags.
    # It returns a triple of inject_flags, env_flags, build_system_flags.
    # The flags returned as inject_flags are injected through the spack
    #  compiler wrappers.
    # The flags returned as env_flags are passed to the build system through
    #  the environment variables of the same name.
    # The flags returned as build_system_flags are passed to the build system
    #  package subclass to be turned into the appropriate part of the standard
    #  arguments. This is implemented for build system classes where
    #  appropriate and will otherwise raise a NotImplementedError.

    def flags_to_build_system_args(self, flags):
        # Takes flags as a dict name: list of values
        if any(v for v in flags.values()):
            msg = 'The {0} build system'.format(self.__class__.__name__)
            msg += ' cannot take command line arguments for compiler flags'
            raise NotImplementedError(msg)

    @staticmethod
    def uninstall_by_spec(spec, force=False, deprecator=None):
        if not os.path.isdir(spec.prefix):
            # prefix may not exist, but DB may be inconsistent. Try to fix by
            # removing, but omit hooks.
            specs = spack.store.db.query(spec, installed=True)
            if specs:
                if deprecator:
                    spack.store.db.deprecate(specs[0], deprecator)
                    tty.debug('Deprecating stale DB entry for {0}'
                              .format(spec.short_spec))
                else:
                    spack.store.db.remove(specs[0])
                    tty.debug('Removed stale DB entry for {0}'
                              .format(spec.short_spec))
                return
            else:
                raise InstallError(str(spec) + " is not installed.")

        if not force:
            dependents = spack.store.db.installed_relatives(
                spec, 'parents', True)
            if dependents:
                raise PackageStillNeededError(spec, dependents)

        # Try to get the package for the spec
        try:
            pkg = spec.package
        except spack.repo.UnknownEntityError:
            pkg = None

        # Pre-uninstall hook runs first.
        with spack.store.db.prefix_write_lock(spec):

            if pkg is not None:
                try:
                    spack.hooks.pre_uninstall(spec)
                except Exception as error:
                    if force:
                        error_msg = (
                            "One or more pre_uninstall hooks have failed"
                            " for {0}, but Spack is continuing with the"
                            " uninstall".format(str(spec)))
                        if isinstance(error, spack.error.SpackError):
                            error_msg += (
                                "\n\nError message: {0}".format(str(error)))
                        tty.warn(error_msg)
                        # Note that if the uninstall succeeds then we won't be
                        # seeing this error again and won't have another chance
                        # to run the hook.
                    else:
                        raise

            # Uninstalling in Spack only requires removing the prefix.
            if not spec.external:
                msg = 'Deleting package prefix [{0}]'
                tty.debug(msg.format(spec.short_spec))
                # test if spec is already deprecated, not whether we want to
                # deprecate it now
                deprecated = bool(spack.store.db.deprecator(spec))
                spack.store.layout.remove_install_directory(spec, deprecated)
            # Delete DB entry
            if deprecator:
                msg = 'deprecating DB entry [{0}] in favor of [{1}]'
                tty.debug(msg.format(spec.short_spec, deprecator.short_spec))
                spack.store.db.deprecate(spec, deprecator)
            else:
                msg = 'Deleting DB entry [{0}]'
                tty.debug(msg.format(spec.short_spec))
                spack.store.db.remove(spec)

        if pkg is not None:
            try:
                spack.hooks.post_uninstall(spec)
            except Exception:
                # If there is a failure here, this is our only chance to do
                # something about it: at this point the Spec has been removed
                # from the DB and prefix, so the post-uninstallation hooks
                # will not have another chance to run.
                error_msg = (
                    "One or more post-uninstallation hooks failed for"
                    " {0}, but the prefix has been removed (if it is not"
                    " external).".format(str(spec)))
                tb_msg = traceback.format_exc()
                error_msg += "\n\nThe error:\n\n{0}".format(tb_msg)
                tty.warn(error_msg)

        tty.msg('Successfully uninstalled {0}'.format(spec.short_spec))

    def do_uninstall(self, force=False):
        """Uninstall this package by spec."""
        # delegate to instance-less method.
        Package.uninstall_by_spec(self.spec, force)

    def do_deprecate(self, deprecator, link_fn):
        """Deprecate this package in favor of deprecator spec"""
        spec = self.spec

        # Check whether package to deprecate has active extensions
        if self.extendable:
            view = spack.filesystem_view.YamlFilesystemView(spec.prefix,
                                                            spack.store.layout)
            active_exts = view.extensions_layout.extension_map(spec).values()
            if active_exts:
                short = spec.format('{name}/{hash:7}')
                m = "Spec %s has active extensions\n" % short
                for active in active_exts:
                    m += '        %s\n' % active.format('{name}/{hash:7}')
                    m += "Deactivate extensions before deprecating %s" % short
                tty.die(m)

        # Check whether package to deprecate is an active extension
        if self.is_extension:
            extendee = self.extendee_spec
            view = spack.filesystem_view.YamlFilesystemView(extendee.prefix,
                                                            spack.store.layout)

            if self.is_activated(view):
                short = spec.format('{name}/{hash:7}')
                short_ext = extendee.format('{name}/{hash:7}')
                msg = "Spec %s is an active extension of %s\n" % (short,
                                                                  short_ext)
                msg += "Deactivate %s to be able to deprecate it" % short
                tty.die(msg)

        # Install deprecator if it isn't installed already
        if not spack.store.db.query(deprecator):
            deprecator.package.do_install()

        old_deprecator = spack.store.db.deprecator(spec)
        if old_deprecator:
            # Find this specs yaml file from its old deprecation
            self_yaml = spack.store.layout.deprecated_file_path(spec,
                                                                old_deprecator)
        else:
            self_yaml = spack.store.layout.spec_file_path(spec)

        # copy spec metadata to "deprecated" dir of deprecator
        depr_yaml = spack.store.layout.deprecated_file_path(spec,
                                                            deprecator)
        fsys.mkdirp(os.path.dirname(depr_yaml))
        shutil.copy2(self_yaml, depr_yaml)

        # Any specs deprecated in favor of this spec are re-deprecated in
        # favor of its new deprecator
        for deprecated in spack.store.db.specs_deprecated_by(spec):
            deprecated.package.do_deprecate(deprecator, link_fn)

        # Now that we've handled metadata, uninstall and replace with link
        Package.uninstall_by_spec(spec, force=True, deprecator=deprecator)
        link_fn(deprecator.prefix, spec.prefix)

    def _check_extendable(self):
        if not self.extendable:
            raise ValueError("Package %s is not extendable!" % self.name)

    def _sanity_check_extension(self):
        if not self.is_extension:
            raise ActivationError("This package is not an extension.")

        extendee_package = self.extendee_spec.package
        extendee_package._check_extendable()

        if not extendee_package.installed:
            raise ActivationError(
                "Can only (de)activate extensions for installed packages.")
        if not self.installed:
            raise ActivationError("Extensions must first be installed.")
        if self.extendee_spec.name not in self.extendees:
            raise ActivationError("%s does not extend %s!" %
                                  (self.name, self.extendee.name))

    def do_activate(self, view=None, with_dependencies=True, verbose=True):
        """Called on an extension to invoke the extendee's activate method.

        Commands should call this routine, and should not call
        activate() directly.
        """
        if verbose:
            tty.msg('Activating extension {0} for {1}'.format(
                self.spec.cshort_spec, self.extendee_spec.cshort_spec))

        self._sanity_check_extension()
        if not view:
            view = YamlFilesystemView(
                self.extendee_spec.prefix, spack.store.layout)

        extensions_layout = view.extensions_layout

        extensions_layout.check_extension_conflict(
            self.extendee_spec, self.spec)

        # Activate any package dependencies that are also extensions.
        if with_dependencies:
            for spec in self.dependency_activations():
                if not spec.package.is_activated(view):
                    spec.package.do_activate(
                        view, with_dependencies=with_dependencies,
                        verbose=verbose)

        self.extendee_spec.package.activate(
            self, view, **self.extendee_args)

        extensions_layout.add_extension(self.extendee_spec, self.spec)

        if verbose:
            tty.debug('Activated extension {0} for {1}'.format(
                self.spec.cshort_spec, self.extendee_spec.cshort_spec))

    def dependency_activations(self):
        return (spec for spec in self.spec.traverse(root=False, deptype='run')
                if spec.package.extends(self.extendee_spec))

    def activate(self, extension, view, **kwargs):
        """
        Add the extension to the specified view.

        Package authors can override this function to maintain some
        centralized state related to the set of activated extensions
        for a package.

        Spack internals (commands, hooks, etc.) should call
        do_activate() method so that proper checks are always executed.
        """
        view.merge(extension.spec, ignore=kwargs.get('ignore', None))

    def do_deactivate(self, view=None, **kwargs):
        """Remove this extension package from the specified view. Called
        on the extension to invoke extendee's deactivate() method.

        `remove_dependents=True` deactivates extensions depending on this
        package instead of raising an error.
        """
        self._sanity_check_extension()
        force = kwargs.get('force', False)
        verbose = kwargs.get('verbose', True)
        remove_dependents = kwargs.get('remove_dependents', False)

        if verbose:
            tty.msg('Deactivating extension {0} for {1}'.format(
                self.spec.cshort_spec, self.extendee_spec.cshort_spec))

        if not view:
            view = YamlFilesystemView(
                self.extendee_spec.prefix, spack.store.layout)
        extensions_layout = view.extensions_layout

        # Allow a force deactivate to happen.  This can unlink
        # spurious files if something was corrupted.
        if not force:
            extensions_layout.check_activated(
                self.extendee_spec, self.spec)

            activated = extensions_layout.extension_map(
                self.extendee_spec)
            for name, aspec in activated.items():
                if aspec == self.spec:
                    continue
                for dep in aspec.traverse(deptype='run'):
                    if self.spec == dep:
                        if remove_dependents:
                            aspec.package.do_deactivate(**kwargs)
                        else:
                            msg = ('Cannot deactivate {0} because {1} is '
                                   'activated and depends on it')
                            raise ActivationError(msg.format(
                                self.spec.cshort_spec, aspec.cshort_spec))

        self.extendee_spec.package.deactivate(
            self, view, **self.extendee_args)

        # redundant activation check -- makes SURE the spec is not
        # still activated even if something was wrong above.
        if self.is_activated(view):
            extensions_layout.remove_extension(
                self.extendee_spec, self.spec)

        if verbose:
            tty.debug('Deactivated extension {0} for {1}'.format(
                self.spec.cshort_spec, self.extendee_spec.cshort_spec))

    def deactivate(self, extension, view, **kwargs):
        """
        Remove all extension files from the specified view.

        Package authors can override this method to support other
        extension mechanisms.  Spack internals (commands, hooks, etc.)
        should call do_deactivate() method so that proper checks are
        always executed.
        """
        view.unmerge(extension.spec, ignore=kwargs.get('ignore', None))

    def view(self):
        """Create a view with the prefix of this package as the root.
        Extensions added to this view will modify the installation prefix of
        this package.
        """
        return YamlFilesystemView(self.prefix, spack.store.layout)

    def do_restage(self):
        """Reverts expanded/checked out source to a pristine state."""
        self.stage.restage()

    def do_clean(self):
        """Removes the package's build stage and source tarball."""
        for patch in self.spec.patches:
            patch.clean()

        self.stage.destroy()

    def format_doc(self, **kwargs):
        """Wrap doc string at 72 characters and format nicely"""
        indent = kwargs.get('indent', 0)

        if not self.__doc__:
            return ""

        doc = re.sub(r'\s+', ' ', self.__doc__)
        lines = textwrap.wrap(doc, 72)
        results = six.StringIO()
        for line in lines:
            results.write((" " * indent) + line + "\n")
        return results.getvalue()

    @property
    def all_urls(self):
        """A list of all URLs in a package.

        Check both class-level and version-specific URLs.

        Returns:
            list: a list of URLs
        """
        urls = []
        if hasattr(self, 'url') and self.url:
            urls.append(self.url)

        # fetch from first entry in urls to save time
        if hasattr(self, 'urls') and self.urls:
            urls.append(self.urls[0])

        for args in self.versions.values():
            if 'url' in args:
                urls.append(args['url'])
        return urls

    def fetch_remote_versions(self, concurrency=128):
        """Find remote versions of this package.

        Uses ``list_url`` and any other URLs listed in the package file.

        Returns:
            dict: a dictionary mapping versions to URLs
        """
        if not self.all_urls:
            return {}

        try:
            return spack.util.web.find_versions_of_archive(
                self.all_urls, self.list_url, self.list_depth, concurrency
            )
        except spack.util.web.NoNetworkConnectionError as e:
            tty.die("Package.fetch_versions couldn't connect to:", e.url,
                    e.message)

    @property
    def rpath(self):
        """Get the rpath this package links with, as a list of paths."""
        rpaths = [self.prefix.lib, self.prefix.lib64]
        deps = self.spec.dependencies(deptype='link')
        rpaths.extend(d.prefix.lib for d in deps
                      if os.path.isdir(d.prefix.lib))
        rpaths.extend(d.prefix.lib64 for d in deps
                      if os.path.isdir(d.prefix.lib64))
        return rpaths

    @property
    def rpath_args(self):
        """
        Get the rpath args as a string, with -Wl,-rpath, for each element
        """
        return " ".join("-Wl,-rpath,%s" % p for p in self.rpath)

    @on_package_attributes(run_tests=True)
    def _run_default_build_time_test_callbacks(self):
        """Tries to call all the methods that are listed in the attribute
        ``build_time_test_callbacks`` if ``self.run_tests is True``.

        If ``build_time_test_callbacks is None`` returns immediately.
        """
        if self.build_time_test_callbacks is None:
            return

        for name in self.build_time_test_callbacks:
            try:
                fn = getattr(self, name)
                tty.msg('RUN-TESTS: build-time tests [{0}]'.format(name))
                fn()
            except AttributeError:
                msg = 'RUN-TESTS: method not implemented [{0}]'
                tty.warn(msg.format(name))

    @on_package_attributes(run_tests=True)
    def _run_default_install_time_test_callbacks(self):
        """Tries to call all the methods that are listed in the attribute
        ``install_time_test_callbacks`` if ``self.run_tests is True``.

        If ``install_time_test_callbacks is None`` returns immediately.
        """
        if self.install_time_test_callbacks is None:
            return

        for name in self.install_time_test_callbacks:
            try:
                fn = getattr(self, name)
                tty.msg('RUN-TESTS: install-time tests [{0}]'.format(name))
                fn()
            except AttributeError:
                msg = 'RUN-TESTS: method not implemented [{0}]'
                tty.warn(msg.format(name))


def test_process(pkg, kwargs):
    with tty.log.log_output(pkg.test_log_file) as logger:
        with logger.force_echo():
            tty.msg('Testing package {0}'
                    .format(pkg.test_suite.test_pkg_id(pkg.spec)))

        # use debug print levels for log file to record commands
        old_debug = tty.is_debug()
        tty.set_debug(True)

        # run test methods from the package and all virtuals it
        # provides virtuals have to be deduped by name
        v_names = list(set([vspec.name
                            for vspec in pkg.virtuals_provided]))

        # hack for compilers that are not dependencies (yet)
        # TODO: this all eventually goes away
        c_names = ('gcc', 'intel', 'intel-parallel-studio', 'pgi')
        if pkg.name in c_names:
            v_names.extend(['c', 'cxx', 'fortran'])
        if pkg.spec.satisfies('llvm+clang'):
            v_names.extend(['c', 'cxx'])

        test_specs = [pkg.spec] + [spack.spec.Spec(v_name)
                                   for v_name in sorted(v_names)]

        try:
            with fsys.working_dir(
                    pkg.test_suite.test_dir_for_spec(pkg.spec)):
                for spec in test_specs:
                    pkg.test_suite.current_test_spec = spec
                    # Fail gracefully if a virtual has no package/tests
                    try:
                        spec_pkg = spec.package
                    except spack.repo.UnknownPackageError:
                        continue

                    # copy test data into test data dir
                    data_source = Prefix(spec_pkg.package_dir).test
                    data_dir = pkg.test_suite.current_test_data_dir
                    if (os.path.isdir(data_source) and
                            not os.path.exists(data_dir)):
                        # We assume data dir is used read-only
                        # maybe enforce this later
                        shutil.copytree(data_source, data_dir)

                    # grab the function for each method so we can call
                    # it with the package
                    test_fn = spec_pkg.__class__.test
                    if not isinstance(test_fn, types.FunctionType):
                        test_fn = test_fn.__func__

                    # Run the tests
                    test_fn(pkg)

            # If fail-fast was on, we error out above
            # If we collect errors, raise them in batch here
            if pkg.test_failures:
                raise TestFailure(pkg.test_failures)

        finally:
            # reset debug level
            tty.set_debug(old_debug)


inject_flags = PackageBase.inject_flags
env_flags = PackageBase.env_flags
build_system_flags = PackageBase.build_system_flags


class BundlePackage(PackageBase):
    """General purpose bundle, or no-code, package class."""
    #: There are no phases by default but the property is required to support
    #: post-install hooks (e.g., for module generation).
    phases = []  # type: List[str]
    #: This attribute is used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = 'BundlePackage'

    #: Bundle packages do not have associated source or binary code.
    has_code = False


class Package(PackageBase):
    """General purpose class with a single ``install``
    phase that needs to be coded by packagers.
    """
    #: The one and only phase
    phases = ['install']
    #: This attribute is used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = 'Package'
    # This will be used as a registration decorator in user
    # packages, if need be
    run_after('install')(PackageBase.sanity_check_prefix)


def install_dependency_symlinks(pkg, spec, prefix):
    """
    Execute a dummy install and flatten dependencies.

    This routine can be used in a ``package.py`` definition by setting
    ``install = install_dependency_symlinks``.

    This feature comes in handy for creating a common location for the
    the installation of third-party libraries.
    """
    flatten_dependencies(spec, prefix)


def use_cray_compiler_names():
    """Compiler names for builds that rely on cray compiler names."""
    os.environ['CC'] = 'cc'
    os.environ['CXX'] = 'CC'
    os.environ['FC'] = 'ftn'
    os.environ['F77'] = 'ftn'


def flatten_dependencies(spec, flat_dir):
    """Make each dependency of spec present in dir via symlink."""
    for dep in spec.traverse(root=False):
        name = dep.name

        dep_path = spack.store.layout.path_for_spec(dep)
        dep_files = LinkTree(dep_path)

        os.mkdir(flat_dir + '/' + name)

        conflict = dep_files.find_conflict(flat_dir + '/' + name)
        if conflict:
            raise DependencyConflictError(conflict)

        dep_files.merge(flat_dir + '/' + name)


def possible_dependencies(*pkg_or_spec, **kwargs):
    """Get the possible dependencies of a number of packages.

    See ``PackageBase.possible_dependencies`` for details.
    """
    packages = []
    for pos in pkg_or_spec:
        if isinstance(pos, PackageMeta):
            packages.append(pos)
            continue

        if not isinstance(pos, spack.spec.Spec):
            pos = spack.spec.Spec(pos)

        if spack.repo.path.is_virtual(pos.name):
            packages.extend(
                p.package_class
                for p in spack.repo.path.providers_for(pos.name)
            )
            continue
        else:
            packages.append(pos.package_class)

    visited = {}
    for pkg in packages:
        pkg.possible_dependencies(visited=visited, **kwargs)

    return visited


class FetchError(spack.error.SpackError):
    """Raised when something goes wrong during fetch."""

    def __init__(self, message, long_msg=None):
        super(FetchError, self).__init__(message, long_msg)


class PackageStillNeededError(InstallError):
    """Raised when package is still needed by another on uninstall."""
    def __init__(self, spec, dependents):
        super(PackageStillNeededError, self).__init__("Cannot uninstall %s" %
                                                      spec)
        self.spec = spec
        self.dependents = dependents


class PackageError(spack.error.SpackError):
    """Raised when something is wrong with a package definition."""
    def __init__(self, message, long_msg=None):
        super(PackageError, self).__init__(message, long_msg)


class PackageVersionError(PackageError):
    """Raised when a version URL cannot automatically be determined."""
    def __init__(self, version):
        super(PackageVersionError, self).__init__(
            "Cannot determine a URL automatically for version %s" % version,
            "Please provide a url for this version in the package.py file.")


class NoURLError(PackageError):
    """Raised when someone tries to build a URL for a package with no URLs."""

    def __init__(self, cls):
        super(NoURLError, self).__init__(
            "Package %s has no version with a URL." % cls.__name__)


class InvalidPackageOpError(PackageError):
    """Raised when someone tries perform an invalid operation on a package."""


class ExtensionError(PackageError):
    """Superclass for all errors having to do with extension packages."""


class ActivationError(ExtensionError):
    """Raised when there are problems activating an extension."""
    def __init__(self, msg, long_msg=None):
        super(ActivationError, self).__init__(msg, long_msg)


class DependencyConflictError(spack.error.SpackError):
    """Raised when the dependencies cannot be flattened as asked for."""
    def __init__(self, conflict):
        super(DependencyConflictError, self).__init__(
            "%s conflicts with another file in the flattened directory." % (
                conflict))
