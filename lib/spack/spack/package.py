# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This is where most of the action happens in Spack.

The spack package class structure is based strongly on Homebrew
(http://brew.sh/), mainly because Homebrew makes it very easy to create
packages.

"""
import base64
import contextlib
import copy
import functools
import glob
import hashlib
import inspect
import os
import re
import shutil
import sys
import textwrap
import time
from six import StringIO
from six import string_types
from six import with_metaclass
from ordereddict_backport import OrderedDict

import llnl.util.tty as tty

import spack.config
import spack.paths
import spack.store
import spack.compilers
import spack.directives
import spack.directory_layout
import spack.error
import spack.fetch_strategy as fs
import spack.hooks
import spack.mirror
import spack.mixins
import spack.repo
import spack.url
import spack.util.web
import spack.multimethod
import spack.binary_distribution as binary_distribution

from llnl.util.filesystem import mkdirp, touch, chgrp
from llnl.util.filesystem import working_dir, install_tree, install
from llnl.util.lang import memoized
from llnl.util.link_tree import LinkTree
from llnl.util.tty.log import log_output
from llnl.util.tty.color import colorize
from spack.filesystem_view import YamlFilesystemView
from spack.util.executable import which
from spack.stage import Stage, ResourceStage, StageComposite
from spack.util.environment import dump_environment
from spack.util.package_hash import package_hash
from spack.version import Version
from spack.package_prefs import get_package_dir_permissions, get_package_group

"""Allowed URL schemes for spack packages."""
_ALLOWED_URL_SCHEMES = ["http", "https", "ftp", "file", "git"]


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
        pass

    def _on_phase_exit(self, instance):
        # If a phase has a matching last_phase attribute,
        # stop the installation process raising a StopIteration
        if getattr(instance, 'last_phase', None) == self.name:
            raise StopIteration('Stopping at \'{0}\' phase'.format(self.name))

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


class PackageMeta(
    spack.directives.DirectiveMeta,
    spack.mixins.PackageMixinsMeta
):
    """Conveniently transforms attributes to permit extensible phases

    Iterates over the attribute 'phases' and creates / updates private
    InstallPhase attributes in the class that is being initialized
    """
    phase_fmt = '_InstallPhase_{0}'

    _InstallPhase_run_before = {}
    _InstallPhase_run_after = {}

    def __new__(cls, name, bases, attr_dict):

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
                view.link(src, dst)

    def remove_files_from_view(self, view, merge_map):
        """Given a map of package files to files currently linked in the view,
        remove the files from the view. The default implementation removes all
        files. Alternative implementations may not remove all files. For
        example if two packages include the same file, it should only be
        removed when both packages are removed.
        """
        for src, dst in merge_map.items():
            view.remove_file(src, dst)


class PackageBase(with_metaclass(PackageMeta, PackageViewMixin, object)):
    """This is the superclass for all spack packages.

    ***The Package class***

    A package defines how to fetch, verify (via, e.g., sha256), build,
    and install a piece of software.  A Package also defines what other
    packages it depends on, so that dependencies can be installed along
    with the package itself.  Packages are written in pure python by
    users of Spack.

    There are two main parts of a Spack package:

      1. **The package class**.  Classes contain ``directives``, which are
         special functions, that add metadata (versions, patches,
         dependencies, and other information) to packages (see
         ``directives.py``). Directives provide the constraints that are
         used as input to the concretizer.

      2. **Package instances**. Once instantiated, a package is
         essentially an installer for a particular piece of
         software. Spack calls methods like ``do_install()`` on the
         ``Package`` object, and it uses those to drive user-implemented
         methods like ``patch()``, ``install()``, and other build steps.
         To install software, An instantiated package needs a *concrete*
         spec, which guides the behavior of the various install methods.

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

       p.do_fetch()              # downloads tarball from a URL
       p.do_stage()              # expands tarball in a temp directory
       p.do_patch()              # applies patches to expanded source
       p.do_install()            # calls package's install() function
       p.do_uninstall()          # removes install directory

    There are also some other commands that clean the build area:

    .. code-block:: python

       p.do_clean()              # removes the stage directory entirely
       p.do_restage()            # removes the build directory and
                                 # re-expands the archive.

    The convention used here is that a ``do_*`` function is intended to be
    called internally by Spack commands (in spack.cmd).  These aren't for
    package writers to override, and doing so may break the functionality
    of the Package class.

    Package creators have a lot of freedom, and they could technically
    override anything in this class.  That is not usually required.

    For most use cases.  Package creators typically just add attributes
    like ``url`` and ``homepage``, or functions like ``install()``.
    There are many custom ``Package`` subclasses in the
    ``spack.build_systems`` package that make things even easier for
    specific build systems.

    """
    #
    # These are default values for instance variables.
    #

    #: By default we build in parallel.  Subclasses can override this.
    parallel = True

    #: # jobs to use for parallel make. If set, overrides default of ncpus.
    make_jobs = None

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
    sanity_check_is_file = []

    #: List of prefix-relative directory paths (or a single path). If
    #: these do not exist after install, or if they exist but are not
    #: directories, sanity checks will fail.
    sanity_check_is_dir = []

    #: List of glob expressions. Each expression must either be
    #: absolute or relative to the package source path.
    #: Matching artifacts found at the end of the build process will
    #: be copied in the same directory tree as build.env and build.out.
    archive_files = []

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
    license_files = []

    #: List of strings. Environment variables that can be set to tell the
    #: software where to look for a license if it is not in the usual location.
    #: Defaults to the empty list.
    license_vars = []

    #: String. A URL pointing to license setup instructions for the software.
    #: Defaults to the empty string.
    license_url = ''

    #: Verbosity level, preserved across installs.
    _verbose = None

    #: index of patches by sha256 sum, built lazily
    _patches_by_hash = None

    #: List of strings which contains GitHub usernames of package maintainers.
    #: Do not include @ here in order not to unnecessarily ping the users.
    maintainers = []

    #: List of attributes which affect do not affect a package's content.
    metadata_attrs = ['homepage', 'url', 'list_url', 'extendable', 'parallel',
                      'make_jobs']

    def __init__(self, spec):
        # this determines how the package should be built.
        self.spec = spec

        # Name of package is the name of its module, without the
        # containing module names.
        self.name = self.module.__name__
        if '.' in self.name:
            self.name = self.name[self.name.rindex('.') + 1:]

        # Allow custom staging paths for packages
        self.path = None

        # Check versions in the versions dict.
        for v in self.versions:
            assert (isinstance(v, Version))

        # Check version descriptors
        for v in sorted(self.versions):
            assert (isinstance(self.versions[v], dict))

        # Version-ize the keys in versions dict
        try:
            self.versions = dict((Version(v), h)
                                 for v, h in self.versions.items())
        except ValueError as e:
            raise ValueError("In package %s: %s" % (self.name, e.message))

        # Set a default list URL (place to find available versions)
        if not hasattr(self, 'list_url'):
            self.list_url = None

        if not hasattr(self, 'list_depth'):
            self.list_depth = 0

        # init internal variables
        self._stage = None
        self._fetcher = None

        # Set up timing variables
        self._fetch_time = 0.0
        self._total_time = 0.0

        if self.is_extension:
            spack.repo.get(self.extendee_spec)._check_extendable()

        super(PackageBase, self).__init__()

    def possible_dependencies(
            self, transitive=True, expand_virtuals=True, visited=None):
        """Return set of possible dependencies of this package.

        Note: the set returned *includes* the package itself.

        Args:
            transitive (bool): return all transitive dependencies if True,
                only direct dependencies if False.
            expand_virtuals (bool): expand virtual dependencies into all
                possible implementations.
            visited (set): set of names of dependencies visited so far.
        """
        if visited is None:
            visited = set([self.name])

        for i, name in enumerate(self.dependencies):
            if spack.repo.path.is_virtual(name):
                if expand_virtuals:
                    providers = spack.repo.path.providers_for(name)
                    dep_names = [spec.name for spec in providers]
                else:
                    visited.add(name)
                    continue
            else:
                dep_names = [name]

            for dep_name in dep_names:
                if dep_name not in visited:
                    visited.add(dep_name)
                    if transitive:
                        pkg = spack.repo.get(dep_name)
                        pkg.possible_dependencies(
                            transitive, expand_virtuals, visited)

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
            raise ValueError("Can only get of package with concrete version.")
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
        default_url = getattr(self, 'url', None)

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
        resource_mirror = spack.mirror.mirror_archive_path(
            self.spec, fetcher, resource.name)
        stage = ResourceStage(resource.fetcher,
                              root=root_stage,
                              resource=resource,
                              name=resource_stage_folder,
                              mirror_path=resource_mirror,
                              path=self.path)
        return stage

    def _make_root_stage(self, fetcher):
        # Construct a mirror path (TODO: get this out of package.py)
        mp = spack.mirror.mirror_archive_path(self.spec, fetcher)
        # Construct a path where the stage should build..
        s = self.spec
        stage_name = "%s-%s-%s" % (s.name, s.version, s.dag_hash())

        def download_search():
            dynamic_fetcher = fs.from_list_url(self)
            return [dynamic_fetcher] if dynamic_fetcher else []

        stage = Stage(fetcher, mirror_path=mp, name=stage_name, path=self.path,
                      search_fn=download_search)
        return stage

    def _make_stage(self):
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
        if not self.spec.concrete:
            raise ValueError("Can only get a stage for a concrete package.")
        if self._stage is None:
            self._stage = self._make_stage()
        return self._stage

    @stage.setter
    def stage(self, stage):
        """Allow a stage object to be set to override the default."""
        self._stage = stage

    @property
    def env_path(self):
        if self.stage.source_path is None:
            return None
        else:
            return os.path.join(self.stage.source_path, 'spack-build.env')

    @property
    def log_path(self):
        if self.stage.source_path is None:
            return None
        else:
            return os.path.join(self.stage.source_path, 'spack-build.out')

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
            raise ValueError(
                "Can only get a fetcher for a package with concrete versions.")
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

    def do_fetch(self, mirror_only=False):
        """
        Creates a stage directory and downloads the tarball for this package.
        Working directory will be set to the stage directory.
        """
        if not self.spec.concrete:
            raise ValueError("Can only fetch concrete packages.")

        start_time = time.time()
        checksum = spack.config.get('config:checksum')
        if checksum and self.version not in self.versions:
            tty.warn("There is no checksum on file to fetch %s safely." %
                     self.spec.cformat('$_$@'))

            # Ask the user whether to skip the checksum if we're
            # interactive, but just fail if non-interactive.
            ck_msg = "Add a checksum or use --no-checksum to skip this check."
            ignore_checksum = False
            if sys.stdout.isatty():
                ignore_checksum = tty.get_yes_or_no("  Fetch anyway?",
                                                    default=False)
                if ignore_checksum:
                    tty.msg("Fetching with no checksum.", ck_msg)

            if not ignore_checksum:
                raise FetchError("Will not fetch %s" %
                                 self.spec.format('$_$@'), ck_msg)

        self.stage.create()
        self.stage.fetch(mirror_only)
        self._fetch_time = time.time() - start_time

        if checksum and self.version in self.versions:
            self.stage.check()

        self.stage.cache_local()

        for patch in self.spec.patches:
            patch.fetch(self.stage)

    def do_stage(self, mirror_only=False):
        """Unpacks and expands the fetched tarball."""
        if not self.spec.concrete:
            raise ValueError("Can only stage concrete packages.")

        self.do_fetch(mirror_only)     # this will create the stage
        self.stage.expand_archive()

        if not os.listdir(self.stage.path):
            raise FetchError("Archive was empty for %s" % self.name)

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
            tty.msg("No patches needed for %s" % self.name)
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
            tty.msg("Patching failed last time. Restaging.")
            self.stage.restage()

        # If this file exists, then we already applied all the patches.
        if os.path.isfile(good_file):
            tty.msg("Already patched %s" % self.name)
            return
        elif os.path.isfile(no_patches_file):
            tty.msg("No patches needed for %s" % self.name)
            return

        # Apply all the patches for specs that match this one
        patched = False
        for patch in patches:
            try:
                with working_dir(self.stage.source_path):
                    patch.apply(self.stage)
                tty.msg('Applied patch %s' % patch.path_or_url)
                patched = True
            except spack.error.SpackError:
                # Touch bad file if anything goes wrong.
                tty.msg('Patch %s failed.' % patch.path_or_url)
                touch(bad_file)
                raise

        if has_patch_fun:
            try:
                with working_dir(self.stage.source_path):
                    self.patch()
                tty.msg("Ran patch() for %s" % self.name)
                patched = True
            except spack.multimethod.NoSuchMethodError:
                # We are running a multimethod without a default case.
                # If there's no default it means we don't need to patch.
                if not patched:
                    # if we didn't apply a patch from a patch()
                    # directive, AND the patch function didn't apply, say
                    # no patches are needed.  Otherwise, we already
                    # printed a message for each patch.
                    tty.msg("No patches needed for %s" % self.name)
            except spack.error.SpackError:
                tty.msg("patch() function failed for %s" % self.name)
                touch(bad_file)
                raise

        # Get rid of any old failed file -- patches have either succeeded
        # or are not needed.  This is mostly defensive -- it's needed
        # if the restage() method doesn't clean *everything* (e.g., for a repo)
        if os.path.isfile(bad_file):
            os.remove(bad_file)

        # touch good or no patches file so that we skip next time.
        if patched:
            touch(good_file)
        else:
            touch(no_patches_file)

    def content_hash(self, content=None):
        """Create a hash based on the sources and logic used to build the
        package. This includes the contents of all applied patches and the
        contents of applicable functions in the package subclass."""
        if not self.spec.concrete:
            err_msg = ("Cannot invoke content_hash on a package"
                       " if the associated spec is not concrete")
            raise spack.error.SpackError(err_msg)

        hash_content = list()
        source_id = fs.for_package_version(self, self.version).source_id()
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
        return base64.b32encode(
            hashlib.sha256(bytes().join(
                sorted(hash_content))).digest()).lower()

    def do_fake_install(self):
        """Make a fake install directory containing fake executables,
        headers, and libraries."""

        command = self.name
        header = self.name
        library = self.name

        # Avoid double 'lib' for packages whose names already start with lib
        if not self.name.startswith('lib'):
            library = 'lib' + library

        dso_suffix = '.dylib' if sys.platform == 'darwin' else '.so'
        chmod = which('chmod')

        # Install fake command
        mkdirp(self.prefix.bin)
        touch(os.path.join(self.prefix.bin, command))
        chmod('+x', os.path.join(self.prefix.bin, command))

        # Install fake header file
        mkdirp(self.prefix.include)
        touch(os.path.join(self.prefix.include, header + '.h'))

        # Install fake shared and static libraries
        mkdirp(self.prefix.lib)
        for suffix in [dso_suffix, '.a']:
            touch(os.path.join(self.prefix.lib, library + suffix))

        # Install fake man page
        mkdirp(self.prefix.man.man1)

        packages_dir = spack.store.layout.build_packages_path(self.spec)
        dump_packages(self.spec, packages_dir)

    def _has_make_target(self, target):
        """Checks to see if 'target' is a valid target in a Makefile.

        Parameters:
            target (str): the target to check for

        Returns:
            bool: True if 'target' is found, else False
        """
        make = inspect.getmodule(self).make

        # Check if we have a Makefile
        for makefile in ['GNUmakefile', 'Makefile', 'makefile']:
            if os.path.exists(makefile):
                break
        else:
            tty.msg('No Makefile found in the build directory')
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
                tty.msg("Target '" + target + "' not found in " + makefile)
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
            tty.msg('No Ninja build script found in the build directory')
            return False

        # Get a list of all targets in the Ninja build script
        # https://ninja-build.org/manual.html#_extra_tools
        all_targets = ninja('-t', 'targets', 'all', output=str).split('\n')

        # Check if 'target' is a valid target
        matches = [line for line in all_targets
                   if line.startswith(target + ':')]

        if not matches:
            tty.msg("Target '" + target + "' not found in build.ninja")
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
        for when_spec, resource_list in self.resources.items():
            if when_spec in self.spec:
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

    def _process_external_package(self, explicit):
        """Helper function to process external packages.

        Runs post install hooks and registers the package in the DB.

        Args:
            explicit (bool): if the package was requested explicitly by
                the user, False if it was pulled in as a dependency of an
                explicit package.
        """
        if self.spec.external_module:
            message = '{s.name}@{s.version} : has external module in {module}'
            tty.msg(message.format(s=self, module=self.spec.external_module))
            message = '{s.name}@{s.version} : is actually installed in {path}'
            tty.msg(message.format(s=self, path=self.spec.external_path))
        else:
            message = '{s.name}@{s.version} : externally installed in {path}'
            tty.msg(message.format(s=self, path=self.spec.external_path))
        try:
            # Check if the package was already registered in the DB
            # If this is the case, then just exit
            rec = spack.store.db.get_record(self.spec)
            message = '{s.name}@{s.version} : already registered in DB'
            tty.msg(message.format(s=self))
            # Update the value of rec.explicit if it is necessary
            self._update_explicit_entry_in_db(rec, explicit)

        except KeyError:
            # If not register it and generate the module file
            # For external packages we just need to run
            # post-install hooks to generate module files
            message = '{s.name}@{s.version} : generating module file'
            tty.msg(message.format(s=self))
            spack.hooks.post_install(self.spec)
            # Add to the DB
            message = '{s.name}@{s.version} : registering into DB'
            tty.msg(message.format(s=self))
            spack.store.db.add(self.spec, None, explicit=explicit)

    def _update_explicit_entry_in_db(self, rec, explicit):
        if explicit and not rec.explicit:
            with spack.store.db.write_transaction():
                rec = spack.store.db.get_record(self.spec)
                rec.explicit = True
                message = '{s.name}@{s.version} : marking the package explicit'
                tty.msg(message.format(s=self))

    def try_install_from_binary_cache(self, explicit):
        tty.msg('Searching for binary cache of %s' % self.name)
        specs = binary_distribution.get_specs()
        binary_spec = spack.spec.Spec.from_dict(self.spec.to_dict())
        binary_spec._mark_concrete()
        if binary_spec not in specs:
            return False
        tty.msg('Installing %s from binary cache' % self.name)
        tarball = binary_distribution.download_tarball(binary_spec)
        binary_distribution.extract_tarball(
            binary_spec, tarball, allow_root=False,
            unsigned=False, force=False)
        spack.store.db.add(
            self.spec, spack.store.layout, explicit=explicit)
        return True

    def do_install(self,
                   keep_prefix=False,
                   keep_stage=False,
                   install_source=False,
                   install_deps=True,
                   skip_patch=False,
                   verbose=False,
                   make_jobs=None,
                   fake=False,
                   explicit=False,
                   tests=False,
                   dirty=None,
                   **kwargs):
        """Called by commands to install a package and its dependencies.

        Package implementations should override install() to describe
        their build process.

        Args:
            keep_prefix (bool): Keep install prefix on failure. By default,
                destroys it.
            keep_stage (bool): By default, stage is destroyed only if there
                are no exceptions during build. Set to True to keep the stage
                even with exceptions.
            install_source (bool): By default, source is not installed, but
                for debugging it might be useful to keep it around.
            install_deps (bool): Install dependencies before installing this
                package
            skip_patch (bool): Skip patch stage of build if True.
            verbose (bool): Display verbose build output (by default,
                suppresses it)
            make_jobs (int): Number of make jobs to use for install. Default
                is ncpus
            fake (bool): Don't really build; install fake stub files instead.
            explicit (bool): True if package was explicitly installed, False
                if package was implicitly installed (as a dependency).
            tests (bool or list or set): False to run no tests, True to test
                all packages, or a list of package names to run tests for some
            dirty (bool): Don't clean the build environment before installing.
            force (bool): Install again, even if already installed.
        """
        if not self.spec.concrete:
            raise ValueError("Can only install concrete packages: %s."
                             % self.spec.name)

        # For external packages the workflow is simplified, and basically
        # consists in module file generation and registration in the DB
        if self.spec.external:
            return self._process_external_package(explicit)

        restage = kwargs.get('restage', False)
        partial = self.check_for_unfinished_installation(keep_prefix, restage)

        # Ensure package is not already installed
        layout = spack.store.layout
        with spack.store.db.prefix_read_lock(self.spec):
            if partial:
                tty.msg(
                    "Continuing from partial install of %s" % self.name)
            elif layout.check_installed(self.spec):
                msg = '{0.name} is already installed in {0.prefix}'
                tty.msg(msg.format(self))
                rec = spack.store.db.get_record(self.spec)
                # In case the stage directory has already been created,
                # this ensures it's removed after we checked that the spec
                # is installed
                if keep_stage is False:
                    self.stage.destroy()
                return self._update_explicit_entry_in_db(rec, explicit)

        self._do_install_pop_kwargs(kwargs)

        # First, install dependencies recursively.
        if install_deps:
            tty.debug('Installing {0} dependencies'.format(self.name))
            for dep in self.spec.traverse(order='post', root=False):
                dep.package.do_install(
                    install_deps=False,
                    explicit=False,
                    keep_prefix=keep_prefix,
                    keep_stage=keep_stage,
                    install_source=install_source,
                    fake=fake,
                    skip_patch=skip_patch,
                    verbose=verbose,
                    make_jobs=make_jobs,
                    tests=tests,
                    dirty=dirty,
                    **kwargs)

        tty.msg(colorize('@*{Installing} @*g{%s}' % self.name))

        if kwargs.get('use_cache', True):
            if self.try_install_from_binary_cache(explicit):
                tty.msg('Successfully installed %s from binary cache'
                        % self.name)
                print_pkg(self.prefix)
                spack.hooks.post_install(self.spec)
                return

            tty.msg('No binary for %s found: installing from source'
                    % self.name)

        # Set run_tests flag before starting build
        self.run_tests = (tests is True or
                          tests and self.name in tests)

        # Set parallelism before starting build.
        self.make_jobs = make_jobs

        # Then install the package itself.
        def build_process():
            """This implements the process forked for each build.

            Has its own process and python module space set up by
            build_environment.fork().

            This function's return value is returned to the parent process.
            """

            start_time = time.time()
            if not fake:
                if not skip_patch:
                    self.do_patch()
                else:
                    self.do_stage()

            tty.msg(
                'Building {0} [{1}]'.format(self.name, self.build_system_class)
            )

            # get verbosity from do_install() parameter or saved value
            echo = verbose
            if PackageBase._verbose is not None:
                echo = PackageBase._verbose

            self.stage.keep = keep_stage
            with self._stage_and_write_lock():
                # Run the pre-install hook in the child process after
                # the directory is created.
                spack.hooks.pre_install(self.spec)
                if fake:
                    self.do_fake_install()
                else:
                    source_path = self.stage.source_path
                    if install_source and os.path.isdir(source_path):
                        src_target = os.path.join(
                            self.spec.prefix, 'share', self.name, 'src')
                        tty.msg('Copying source to {0}'.format(src_target))
                        install_tree(self.stage.source_path, src_target)

                    # Do the real install in the source directory.
                    with working_dir(self.stage.source_path):
                        # Save the build environment in a file before building.
                        dump_environment(self.env_path)

                        # Spawn a daemon that reads from a pipe and redirects
                        # everything to log_path
                        with log_output(self.log_path, echo, True) as logger:
                            for phase_name, phase_attr in zip(
                                    self.phases, self._InstallPhase_phases):

                                phase = getattr(self, phase_attr)
                                # build systems can dynamically remove phases
                                if phase:
                                    with logger.force_echo():
                                        tty.msg(
                                            "Executing phase: '%s'" %
                                            phase_name)

                                    # Redirect stdout and stderr to daemon pipe
                                    phase(self.spec, self.prefix)

                    echo = logger.echo
                    self.log()

                # Run post install hooks before build stage is removed.
                spack.hooks.post_install(self.spec)

            # Stop timer.
            self._total_time = time.time() - start_time
            build_time = self._total_time - self._fetch_time

            tty.msg("Successfully installed %s" % self.name,
                    "Fetch: %s.  Build: %s.  Total: %s." %
                    (_hms(self._fetch_time), _hms(build_time),
                     _hms(self._total_time)))
            print_pkg(self.prefix)

            # preserve verbosity across runs
            return echo

        # hook that allow tests to inspect this Package before installation
        # see unit_test_check() docs.
        if not self.unit_test_check():
            return

        try:
            # Create the install prefix and fork the build process.
            if not os.path.exists(self.prefix):
                spack.store.layout.create_install_directory(self.spec)
            else:
                # Set the proper group for the prefix
                group = get_package_group(self.spec)
                if group:
                    chgrp(self.prefix, group)
                # Set the proper permissions.
                # This has to be done after group because changing groups blows
                # away the sticky group bit on the directory
                mode = os.stat(self.prefix).st_mode
                perms = get_package_dir_permissions(self.spec)
                if mode != perms:
                    os.chmod(self.prefix, perms)

            # Fork a child to do the actual installation
            # we preserve verbosity settings across installs.
            PackageBase._verbose = spack.build_environment.fork(
                self, build_process, dirty=dirty, fake=fake)

            # If we installed then we should keep the prefix
            keep_prefix = self.last_phase is None or keep_prefix
            # note: PARENT of the build process adds the new package to
            # the database, so that we don't need to re-read from file.
            spack.store.db.add(
                self.spec, spack.store.layout, explicit=explicit
            )
        except spack.directory_layout.InstallDirectoryAlreadyExistsError:
            # Abort install if install directory exists.
            # But do NOT remove it (you'd be overwriting someone else's stuff)
            tty.warn("Keeping existing install prefix in place.")
            raise
        except StopIteration as e:
            # A StopIteration exception means that do_install
            # was asked to stop early from clients
            tty.msg(e.message)
            tty.msg(
                'Package stage directory : {0}'.format(self.stage.source_path)
            )
        finally:
            # Remove the install prefix if anything went wrong during install.
            if not keep_prefix:
                self.remove_prefix()

            # The subprocess *may* have removed the build stage. Mark it
            # not created so that the next time self.stage is invoked, we
            # check the filesystem for it.
            self.stage.created = False

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

    def check_for_unfinished_installation(
            self, keep_prefix=False, restage=False):
        """Check for leftover files from partially-completed prior install to
        prepare for a new install attempt.

        Options control whether these files are reused (vs. destroyed).

        Args:
            keep_prefix (bool): True if the installation prefix needs to be
                kept, False otherwise
            restage (bool): False if the stage has to be kept, True otherwise

        Returns:
            True if the prefix exists but the install is not complete, False
            otherwise.
        """
        if self.spec.external:
            raise ExternalPackageError("Attempted to repair external spec %s" %
                                       self.spec.name)

        with spack.store.db.prefix_write_lock(self.spec):
            try:
                record = spack.store.db.get_record(self.spec)
                installed_in_db = record.installed if record else False
            except KeyError:
                installed_in_db = False

            partial = False
            if not installed_in_db and os.path.isdir(self.prefix):
                if not keep_prefix:
                    self.remove_prefix()
                else:
                    partial = True

        stage_is_managed_in_spack = self.stage.path.startswith(
            spack.paths.stage_path)
        if restage and stage_is_managed_in_spack:
            self.stage.destroy()
            self.stage.create()

        return partial

    def _do_install_pop_kwargs(self, kwargs):
        """Pops kwargs from do_install before starting the installation

        Args:
            kwargs:
              'stop_at': last installation phase to be executed (or None)

        """
        self.last_phase = kwargs.pop('stop_at', None)
        if self.last_phase is not None and self.last_phase not in self.phases:
            tty.die('\'{0}\' is not an allowed phase for package {1}'
                    .format(self.last_phase, self.name))

    def log(self):
        # Copy provenance into the install directory on success
        log_install_path = spack.store.layout.build_log_path(self.spec)
        env_install_path = spack.store.layout.build_env_path(self.spec)
        packages_dir = spack.store.layout.build_packages_path(self.spec)

        # Remove first if we're overwriting another build
        # (can happen with spack setup)
        try:
            # log_install_path and env_install_path are inside this
            shutil.rmtree(packages_dir)
        except Exception:
            # FIXME : this potentially catches too many things...
            pass

        # Archive the whole stdout + stderr for the package
        install(self.log_path, log_install_path)
        # Archive the environment used for the build
        install(self.env_path, env_install_path)
        # Finally, archive files that are specific to each package
        with working_dir(self.stage.source_path):
            errors = StringIO()
            target_dir = os.path.join(
                spack.store.layout.metadata_path(self.spec),
                'archived-files')

            for glob_expr in self.archive_files:
                # Check that we are trying to copy things that are
                # in the source_path tree (not arbitrary files)
                abs_expr = os.path.realpath(glob_expr)
                if os.path.realpath(self.stage.source_path) not in abs_expr:
                    errors.write(
                        '[OUTSIDE SOURCE PATH]: {0}\n'.format(glob_expr)
                    )
                    continue
                # Now that we are sure that the path is within the correct
                # folder, make it relative and check for matches
                if os.path.isabs(glob_expr):
                    glob_expr = os.path.relpath(
                        glob_expr, self.stage.source_path
                    )
                files = glob.glob(glob_expr)
                for f in files:
                    try:
                        target = os.path.join(target_dir, f)
                        # We must ensure that the directory exists before
                        # copying a file in
                        mkdirp(os.path.dirname(target))
                        install(f, target)
                    except Exception:
                        # Here try to be conservative, and avoid discarding
                        # the whole install procedure because of copying a
                        # single file failed
                        errors.write('[FAILED TO ARCHIVE]: {0}'.format(f))

            if errors.getvalue():
                error_file = os.path.join(target_dir, 'errors.txt')
                mkdirp(target_dir)
                with open(error_file, 'w') as err:
                    err.write(errors.getvalue())
                tty.warn('Errors occurred when archiving files.\n\t'
                         'See: {0}'.format(error_file))

        dump_packages(self.spec, packages_dir)

    def sanity_check_prefix(self):
        """This function checks whether install succeeded."""

        def check_paths(path_list, filetype, predicate):
            if isinstance(path_list, string_types):
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
        if self.installed:
            return spack.store.layout.build_log_path(self.spec)
        else:
            return os.path.join(self.stage.source_path, 'spack-build.out')

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

    def setup_environment(self, spack_env, run_env):
        """Set up the compile and runtime environments for a package.

        ``spack_env`` and ``run_env`` are ``EnvironmentModifications``
        objects. Package authors can call methods on them to alter
        the environment within Spack and at runtime.

        Both ``spack_env`` and ``run_env`` are applied within the build
        process, before this package's ``install()`` method is called.

        Modifications in ``run_env`` will *also* be added to the
        generated environment modules for this package.

        Default implementation does nothing, but this can be
        overridden if the package needs a particular environment.

        Example:

        1. Qt extensions need ``QTDIR`` set.

        Args:
            spack_env (EnvironmentModifications): List of environment
                modifications to be applied when this package is built
                within Spack.
            run_env (EnvironmentModifications): List of environment
                modifications to be applied when this package is run outside
                of Spack. These are added to the resulting module file.
        """
        pass

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Set up the environment of packages that depend on this one.

        This is similar to ``setup_environment``, but it is used to
        modify the compile and runtime environments of packages that
        *depend* on this one. This gives packages like Python and
        others that follow the extension model a way to implement
        common environment or compile-time settings for dependencies.

        This is useful if there are some common steps to installing
        all extensions for a certain package.

        Example:

        1. Installing python modules generally requires ``PYTHONPATH`` to point
           to the ``lib/pythonX.Y/site-packages`` directory in the module's
           install prefix. This method could be used to set that variable.

        Args:
            spack_env (EnvironmentModifications): List of environment
                modifications to be applied when the dependent package is
                built within Spack.
            run_env (EnvironmentModifications): List of environment
                modifications to be applied when the dependent package is
                run outside of Spack. These are added to the resulting
                module file.
            dependent_spec (Spec): The spec of the dependent package
                about to be built. This allows the extendee (self) to query
                the dependent's state. Note that *this* package's spec is
                available as ``self.spec``.
        """
        pass

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
    def uninstall_by_spec(spec, force=False):
        if not os.path.isdir(spec.prefix):
            # prefix may not exist, but DB may be inconsistent. Try to fix by
            # removing, but omit hooks.
            specs = spack.store.db.query(spec, installed=True)
            if specs:
                spack.store.db.remove(specs[0])
                tty.msg("Removed stale DB entry for %s" % spec.short_spec)
                return
            else:
                raise InstallError(str(spec) + " is not installed.")

        if not force:
            dependents = spack.store.db.installed_relatives(
                spec, 'parents', True)
            if dependents:
                raise PackageStillNeededError(spec, dependents)

        # Try to get the pcakage for the spec
        try:
            pkg = spec.package
        except spack.repo.UnknownEntityError:
            pkg = None

        # Pre-uninstall hook runs first.
        with spack.store.db.prefix_write_lock(spec):

            if pkg is not None:
                spack.hooks.pre_uninstall(spec)

            # Uninstalling in Spack only requires removing the prefix.
            if not spec.external:
                msg = 'Deleting package prefix [{0}]'
                tty.debug(msg.format(spec.short_spec))
                spack.store.layout.remove_install_directory(spec)
            # Delete DB entry
            msg = 'Deleting DB entry [{0}]'
            tty.debug(msg.format(spec.short_spec))
            spack.store.db.remove(spec)

        if pkg is not None:
            spack.hooks.post_uninstall(spec)

        tty.msg("Successfully uninstalled %s" % spec.short_spec)

    def do_uninstall(self, force=False):
        """Uninstall this package by spec."""
        # delegate to instance-less method.
        Package.uninstall_by_spec(self.spec, force)

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
        results = StringIO()
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

        for args in self.versions.values():
            if 'url' in args:
                urls.append(args['url'])
        return urls

    def fetch_remote_versions(self):
        """Find remote versions of this package.

        Uses ``list_url`` and any other URLs listed in the package file.

        Returns:
            dict: a dictionary mapping versions to URLs
        """
        if not self.all_urls:
            return {}

        try:
            return spack.util.web.find_versions_of_archive(
                self.all_urls, self.list_url, self.list_depth)
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

    build_time_test_callbacks = None

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

    install_time_test_callbacks = None

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


inject_flags = PackageBase.inject_flags
env_flags = PackageBase.env_flags
build_system_flags = PackageBase.build_system_flags


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
    """Execute a dummy install and flatten dependencies"""
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


def dump_packages(spec, path):
    """Dump all package information for a spec and its dependencies.

       This creates a package repository within path for every
       namespace in the spec DAG, and fills the repos wtih package
       files and patch files for every node in the DAG.
    """
    mkdirp(path)

    # Copy in package.py files from any dependencies.
    # Note that we copy them in as they are in the *install* directory
    # NOT as they are in the repository, because we want a snapshot of
    # how *this* particular build was done.
    for node in spec.traverse(deptype=all):
        if node is not spec:
            # Locate the dependency package in the install tree and find
            # its provenance information.
            source = spack.store.layout.build_packages_path(node)
            source_repo_root = os.path.join(source, node.namespace)

            # There's no provenance installed for the source package.  Skip it.
            # User can always get something current from the builtin repo.
            if not os.path.isdir(source_repo_root):
                continue

            # Create a source repo and get the pkg directory out of it.
            try:
                source_repo = spack.repo.Repo(source_repo_root)
                source_pkg_dir = source_repo.dirname_for_package_name(
                    node.name)
            except spack.repo.RepoError:
                tty.warn("Warning: Couldn't copy in provenance for %s" %
                         node.name)

        # Create a destination repository
        dest_repo_root = os.path.join(path, node.namespace)
        if not os.path.exists(dest_repo_root):
            spack.repo.create_repo(dest_repo_root)
        repo = spack.repo.Repo(dest_repo_root)

        # Get the location of the package in the dest repo.
        dest_pkg_dir = repo.dirname_for_package_name(node.name)
        if node is not spec:
            install_tree(source_pkg_dir, dest_pkg_dir)
        else:
            spack.repo.path.dump_provenance(node, dest_pkg_dir)


def print_pkg(message):
    """Outputs a message with a package icon."""
    from llnl.util.tty.color import cwrite
    cwrite('@*g{[+]} ')
    print(message)


def _hms(seconds):
    """Convert time in seconds to hours, minutes, seconds."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    parts = []
    if h:
        parts.append("%dh" % h)
    if m:
        parts.append("%dm" % m)
    if s:
        parts.append("%.2fs" % s)
    return ' '.join(parts)


class FetchError(spack.error.SpackError):
    """Raised when something goes wrong during fetch."""

    def __init__(self, message, long_msg=None):
        super(FetchError, self).__init__(message, long_msg)


class InstallError(spack.error.SpackError):
    """Raised when something goes wrong during install or uninstall."""

    def __init__(self, message, long_msg=None):
        super(InstallError, self).__init__(message, long_msg)


class ExternalPackageError(InstallError):
    """Raised by install() when a package is only for external use."""


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
