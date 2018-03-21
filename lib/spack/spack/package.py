##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""
This is where most of the action happens in Spack.
See the Package docs for detailed instructions on how the class works
and on how to write your own packages.

The spack package structure is based strongly on Homebrew
(http://wiki.github.com/mxcl/homebrew/), mainly because
Homebrew makes it very easy to create packages.  For a complete
rundown on spack and how it differs from homebrew, look at the
README.
"""
import base64
import contextlib
import copy
import functools
import hashlib
import inspect
import itertools
import os
import re
import shutil
import sys
import textwrap
import time
from six import StringIO
from six import string_types
from six import with_metaclass

import llnl.util.tty as tty
import spack
import spack.store
import spack.compilers
import spack.directives
import spack.error
import spack.fetch_strategy as fs
import spack.hooks
import spack.mirror
import spack.mixins
import spack.repository
import spack.url
import spack.util.web
import spack.multimethod
import spack.binary_distribution as binary_distribution

from llnl.util.filesystem import mkdirp, join_path, touch, ancestor
from llnl.util.filesystem import working_dir, install_tree, install
from llnl.util.lang import memoized
from llnl.util.link_tree import LinkTree
from llnl.util.tty.log import log_output
from llnl.util.tty.color import colorize
from spack import directory_layout
from spack.util.executable import which
from spack.stage import Stage, ResourceStage, StageComposite
from spack.util.environment import dump_environment
from spack.util.package_hash import package_hash
from spack.version import Version

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

    def __new__(mcs, name, bases, attr_dict):

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
            checks = getattr(mcs, attr_name)
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
                setattr(mcs, attr_name, {})

        _flush_callbacks('run_before')
        _flush_callbacks('run_after')

        return super(PackageMeta, mcs).__new__(mcs, name, bases, attr_dict)

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


class PackageBase(with_metaclass(PackageMeta, object)):
    """This is the superclass for all spack packages.

    ***The Package class***

    Package is where the bulk of the work of installing packages is done.

    A package defines how to fetch, verfiy (via, e.g., md5), build, and
    install a piece of software.  A Package also defines what other
    packages it depends on, so that dependencies can be installed along
    with the package itself.  Packages are written in pure python.

    Packages are all submodules of spack.packages.  If spack is installed
    in ``$prefix``, all of its python files are in ``$prefix/lib/spack``.
    Most of them are in the spack module, so all the packages live in
    ``$prefix/lib/spack/spack/packages``.

    All you have to do to create a package is make a new subclass of Package
    in this directory.  Spack automatically scans the python files there
    and figures out which one to import when you invoke it.

    **An example package**

    Let's look at the cmake package to start with.  This package lives in
    ``$prefix/var/spack/repos/builtin/packages/cmake/package.py``:

    .. code-block:: python

       from spack import *
       class Cmake(Package):
           homepage  = 'https://www.cmake.org'
           url       = 'http://www.cmake.org/files/v2.8/cmake-2.8.10.2.tar.gz'
           md5       = '097278785da7182ec0aea8769d06860c'

           def install(self, spec, prefix):
               configure('--prefix=%s'   % prefix,
                         '--parallel=%s' % make_jobs)
               make()
               make('install')

    **Naming conventions**

    There are two names you should care about:

    1. The module name, ``cmake``.

       * User will refers to this name, e.g. 'spack install cmake'.
       * It can include ``_``, ``-``, and numbers (it can even start with a
         number).

    2. The class name, "Cmake".  This is formed by converting `-` or
       ``_`` in the module name to camel case.  If the name starts with
       a number, we prefix the class name with ``_``. Examples:

          ===========  ==========
          Module Name  Class Name
          ===========  ==========
          foo_bar      FooBar
          docbook-xml  DocbookXml
          FooBar       Foobar
          3proxy       _3proxy
          ===========  ==========

        The class name is what spack looks for when it loads a package module.

    **Required Attributes**

    Aside from proper naming, here is the bare minimum set of things you
    need when you make a package:

    homepage:
        informational URL, so that users know what they're
        installing.

    url or url_for_version(self, version):
      If url, then the URL of the source archive that spack will fetch.
      If url_for_version(), then a method returning the URL required
      to fetch a particular version.

    install():
        This function tells spack how to build and install the
        software it downloaded.

    **Optional Attributes**

    You can also optionally add these attributes, if needed:

        list_url:
            Webpage to scrape for available version strings. Default is the
            directory containing the tarball; use this if the default isn't
            correct so that invoking 'spack versions' will work for this
            package.

        url_version(self, version):
            When spack downloads packages at particular versions, it just
            converts version to string with str(version).  Override this if
            your package needs special version formatting in its URL.  boost
            is an example of a package that needs this.

    ***Creating Packages***

    As a package creator, you can probably ignore most of the preceding
    information, because you can use the 'spack create' command to do it
    all automatically.

    You as the package creator generally only have to worry about writing
    your install function and specifying dependencies.

    **spack create**

    Most software comes in nicely packaged tarballs, like this one

    http://www.cmake.org/files/v2.8/cmake-2.8.10.2.tar.gz

    Taking a page from homebrew, spack deduces pretty much everything it
    needs to know from the URL above.  If you simply type this::

        spack create http://www.cmake.org/files/v2.8/cmake-2.8.10.2.tar.gz

    Spack will download the tarball, generate an md5 hash, figure out the
    version and the name of the package from the URL, and create a new
    package file for you with all the names and attributes set correctly.

    Once this skeleton code is generated, spack pops up the new package in
    your $EDITOR so that you can modify the parts that need changes.

    **Dependencies**

    If your package requires another in order to build, you can specify that
    like this:

    .. code-block:: python

       class Stackwalker(Package):
           ...
           depends_on("libdwarf")
           ...

    This tells spack that before it builds stackwalker, it needs to build
    the libdwarf package as well.  Note that this is the module name, not
    the class name (The class name is really only used by spack to find
    your package).

    Spack will download an install each dependency before it installs your
    package.  In addtion, it will add -L, -I, and rpath arguments to your
    compiler and linker for each dependency.  In most cases, this allows you
    to avoid specifying any dependencies in your configure or cmake line;
    you can just run configure or cmake without any additional arguments and
    it will find the dependencies automatically.

    **The Install Function**

    The install function is designed so that someone not too terribly familiar
    with Python could write a package installer.  For example, we put a number
    of commands in install scope that you can use almost like shell commands.
    These include make, configure, cmake, rm, rmtree, mkdir, mkdirp, and
    others.

    You can see above in the cmake script that these commands are used to run
    configure and make almost like they're used on the command line.  The
    only difference is that they are python function calls and not shell
    commands.

    It may be puzzling to you where the commands and functions in install live.
    They are NOT instance variables on the class; this would require us to
    type 'self.' all the time and it makes the install code unnecessarily long.
    Rather, spack puts these commands and variables in *module* scope for your
    Package subclass.  Since each package has its own module, this doesn't
    pollute other namespaces, and it allows you to more easily implement an
    install function.

    For a full list of commands and variables available in module scope, see
    the add_commands_to_module() function in this class. This is where most
    of them are created and set on the module.

    **Parallel Builds**

    By default, Spack will run make in parallel when you run make() in your
    install function.  Spack figures out how many cores are available on
    your system and runs make with -j<cores>.  If you do not want this
    behavior, you can explicitly mark a package not to use parallel make:

    .. code-block:: python

       class SomePackage(Package):
           ...
           parallel = False
           ...

    This changes the default behavior so that make is sequential.  If you still
    want to build some parts in parallel, you can do this in your install
    function:

    .. code-block:: python

       make(parallel=True)

    Likewise, if you do not supply parallel = True in your Package, you can
    keep the default parallel behavior and run make like this when you want a
    sequential build:

    .. code-block:: python

       make(parallel=False)

    **Package Lifecycle**

    This section is really only for developers of new spack commands.

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

    Package creators override functions like install() (all of them do this),
    clean() (some of them do this), and others to provide custom behavior.
    """
    #
    # These are default values for instance variables.
    #

    #: By default we build in parallel.  Subclasses can override this.
    parallel = True

    #: # jobs to use for parallel make. If set, overrides default of ncpus.
    make_jobs = spack.build_jobs

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

        # stage used to build this package.
        self._stage = None

        # Init fetch strategy and url to None
        self._fetcher = None
        self.url = getattr(self.__class__, 'url', None)

        # Fix up self.url if this package fetches with a URLFetchStrategy.
        # This makes self.url behave sanely.
        if self.spec.versions.concrete:
            # TODO: this is a really roundabout way of determining the type
            # TODO: of fetch to do. figure out a more sane fetch
            # TODO: strategy/package init order (right now it's conflated with
            # TODO: stage, package, and the tests make assumptions)
            f = fs.for_package_version(self, self.version)
            if isinstance(f, fs.URLFetchStrategy):
                self.url = self.url_for_version(self.spec.version)

        # Set a default list URL (place to find available versions)
        if not hasattr(self, 'list_url'):
            self.list_url = None

        if not hasattr(self, 'list_depth'):
            self.list_depth = 0

        # Set up some internal variables for timing.
        self._fetch_time = 0.0
        self._total_time = 0.0

        if self.is_extension:
            spack.repo.get(self.extendee_spec)._check_extendable()

        self.extra_args = {}

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
            if spack.repo.is_virtual(name):
                if expand_virtuals:
                    providers = spack.repo.providers_for(name)
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

    @property
    def package_dir(self):
        """Return the directory where the package.py file lives."""
        return os.path.abspath(os.path.dirname(self.module.__file__))

    @property
    def global_license_dir(self):
        """Returns the directory where global license files for all
           packages are stored."""
        spack_root = ancestor(__file__, 4)
        return join_path(spack_root, 'etc', 'spack', 'licenses')

    @property
    def global_license_file(self):
        """Returns the path where a global license file for this
           particular package should be stored."""
        if not self.license_files:
            return
        return join_path(self.global_license_dir, self.name,
                         os.path.basename(self.license_files[0]))

    @property
    def version(self):
        if not self.spec.versions.concrete:
            raise ValueError("Can only get of package with concrete version.")
        return self.spec.versions[0]

    @memoized
    def version_urls(self):
        """Return a list of URLs for different versions of this
           package, sorted by version.  A version's URL only appears
           in this list if it has an explicitly defined URL."""
        version_urls = {}
        for v in sorted(self.versions):
            args = self.versions[v]
            if 'url' in args:
                version_urls[v] = args['url']
        return version_urls

    def nearest_url(self, version):
        """Finds the URL for the next lowest version with a URL.
           If there is no lower version with a URL, uses the
           package url property. If that isn't there, uses a
           *higher* URL, and if that isn't there raises an error.
        """
        version_urls = self.version_urls()
        url = getattr(self.__class__, 'url', None)

        for v in version_urls:
            if v > version and url:
                break
            if version_urls[v]:
                url = version_urls[v]
        return url

    # TODO: move this out of here and into some URL extrapolation module?
    def url_for_version(self, version):
        """Returns a URL from which the specified version of this package
        may be downloaded.

        version: class Version
            The version for which a URL is sought.

        See Class Version (version.py)
        """
        if not isinstance(version, Version):
            version = Version(version)

        cls = self.__class__
        if not (hasattr(cls, 'url') or self.version_urls()):
            raise NoURLError(cls)

        # If we have a specific URL for this version, don't extrapolate.
        version_urls = self.version_urls()
        if version in version_urls:
            return version_urls[version]

        # If we have no idea, try to substitute the version.
        return spack.url.substitute_version(
            self.nearest_url(version), self.url_version(version))

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
        return os.path.join(self.stage.source_path, 'spack-build.env')

    @property
    def log_path(self):
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

    def is_activated(self, extensions_layout=None):
        """Return True if package is activated."""
        if not self.is_extension:
            raise ValueError(
                "is_extension called on package that is not an extension.")
        if extensions_layout is None:
            extensions_layout = spack.store.extensions
        exts = extensions_layout.extension_map(self.extendee_spec)
        return (self.name in exts) and (exts[self.name] == self.spec)

    def provides(self, vpkg_name):
        """
        True if this package provides a virtual package with the specified name
        """
        return any(s.name == vpkg_name for s in self.provided)

    @property
    def installed(self):
        return os.path.isdir(self.prefix)

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
        if spack.do_checksum and self.version not in self.versions:
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

        if spack.do_checksum and self.version in self.versions:
            self.stage.check()

        self.stage.cache_local()

    def do_stage(self, mirror_only=False):
        """Unpacks and expands the fetched tarball."""
        if not self.spec.concrete:
            raise ValueError("Can only stage concrete packages.")

        self.do_fetch(mirror_only)     # this will create the stage
        self.stage.expand_archive()

        if not os.listdir(self.stage.path):
            raise FetchError("Archive was empty for %s" % self.name)

    @classmethod
    def lookup_patch(cls, sha256):
        """Look up a patch associated with this package by its sha256 sum.

        Args:
            sha256 (str): sha256 sum of the patch to look up

        Returns:
            (Patch): ``Patch`` object with the given hash, or ``None`` if
                not found.

        To do the lookup, we build an index lazily.  This allows us to
        avoid computing a sha256 for *every* patch and on every package
        load.  With lazy hashing, we only compute hashes on lookup, which
        usually happens at build time.

        """
        if cls._patches_by_hash is None:
            cls._patches_by_hash = {}

            # Add patches from the class
            for cond, patch_list in cls.patches.items():
                for patch in patch_list:
                    cls._patches_by_hash[patch.sha256] = patch

            # and patches on dependencies
            for name, conditions in cls.dependencies.items():
                for cond, dependency in conditions.items():
                    for pcond, patch_list in dependency.patches.items():
                        for patch in patch_list:
                            cls._patches_by_hash[patch.sha256] = patch

        return cls._patches_by_hash.get(sha256, None)

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
        good_file = join_path(archive_dir, '.spack_patched')
        no_patches_file = join_path(archive_dir, '.spack_no_patches')
        bad_file = join_path(archive_dir, '.spack_patch_failed')

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
        for patch in self.patches_to_apply():
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

    def patches_to_apply(self):
        """If the patch set does not change between two invocations of spack,
           then all patches in the set will be applied in the same order"""
        patchesToApply = itertools.chain.from_iterable(
            patch_list
            for spec, patch_list in self.patches.items()
            if self.spec.satisfies(spec))
        return sorted(patchesToApply, key=lambda p: p.path_or_url)

    def content_hash(self, content=None):
        """Create a hash based on the sources and logic used to build the
        package. This includes the contents of all applied patches and the
        contents of applicable functions in the package subclass."""
        hashContent = list()
        source_id = fs.for_package_version(self, self.version).source_id()
        if not source_id:
            # TODO? in cases where a digest or source_id isn't available,
            # should this attempt to download the source and set one? This
            # probably only happens for source repositories which are
            # referenced by branch name rather than tag or commit ID.
            message = 'Missing a source id for {s.name}@{s.version}'
            tty.warn(message.format(s=self))
            hashContent.append(''.encode('utf-8'))
        else:
            hashContent.append(source_id.encode('utf-8'))
        hashContent.extend(':'.join((p.sha256, str(p.level))).encode('utf-8')
                           for p in self.patches_to_apply())
        hashContent.append(package_hash(self.spec, content))
        return base64.b32encode(
            hashlib.sha256(bytes().join(sorted(hashContent))).digest()).lower()

    @property
    def namespace(self):
        namespace, dot, module = self.__module__.rpartition('.')
        return namespace

    def do_fake_install(self):
        """Make a fake install directory containing fake executables,
        headers, and libraries."""

        name = self.name
        library_name = 'lib' + self.name
        dso_suffix = '.dylib' if sys.platform == 'darwin' else '.so'
        chmod = which('chmod')

        mkdirp(self.prefix.bin)
        touch(join_path(self.prefix.bin, name))
        chmod('+x', join_path(self.prefix.bin, name))

        mkdirp(self.prefix.include)
        touch(join_path(self.prefix.include, name + '.h'))

        mkdirp(self.prefix.lib)
        touch(join_path(self.prefix.lib, library_name + dso_suffix))
        touch(join_path(self.prefix.lib, library_name + '.a'))

        mkdirp(self.prefix.man.man1)

        packages_dir = spack.store.layout.build_packages_path(self.spec)
        dump_packages(self.spec, packages_dir)

    def _if_make_target_execute(self, target):
        try:
            # Check if we have a makefile
            file = [x for x in ('Makefile', 'makefile') if os.path.exists(x)]
            file = file.pop()
        except IndexError:
            tty.msg('No Makefile found in the build directory')
            return

        # Check if 'target' is in the makefile
        regex = re.compile('^' + target + ':')
        with open(file, 'r') as f:
            matches = [line for line in f.readlines() if regex.match(line)]

        if not matches:
            tty.msg("Target '" + target + ":' not found in Makefile")
            return

        # Execute target
        inspect.getmodule(self).make(target)

    def _if_ninja_target_execute(self, target):
        # Check if we have a ninja build script
        if not os.path.exists('build.ninja'):
            tty.msg('No ninja build script found in the build directory')
            return

        # Check if 'target' is in the ninja build script
        regex = re.compile('^build ' + target + ':')
        with open('build.ninja', 'r') as f:
            matches = [line for line in f.readlines() if regex.match(line)]

        if not matches:
            tty.msg("Target 'build " + target + ":' not found in build.ninja")
            return

        # Execute target
        inspect.getmodule(self).ninja(target)

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
        spack.store.db.add(self.spec, spack.store.layout, explicit=explicit)
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
                    dirty=dirty,
                    **kwargs)

        tty.msg(colorize('@*{Installing} @*g{%s}' % self.name))

        if kwargs.get('use_cache', False):
            if self.try_install_from_binary_cache(explicit):
                tty.msg('Successfully installed %s from binary cache'
                        % self.name)
                print_pkg(self.prefix)
                spack.hooks.post_install(self.spec)
                return

            tty.msg('No binary for %s found: installing from source'
                    % self.name)

        # Set run_tests flag before starting build.
        self.run_tests = spack.package_testing.check(self.name)

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
                        src_target = join_path(
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

                                with logger.force_echo():
                                    tty.msg(
                                        "Executing phase: '%s'" % phase_name)

                                # Redirect stdout and stderr to daemon pipe
                                phase = getattr(self, phase_attr)
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

        try:
            # Create the install prefix and fork the build process.
            if not os.path.exists(self.prefix):
                spack.store.layout.create_install_directory(self.spec)

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
        except directory_layout.InstallDirectoryAlreadyExistsError:
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

    def check_for_unfinished_installation(
            self, keep_prefix=False, restage=False):
        """Check for leftover files from partially-completed prior install to
           prepare for a new install attempt. Options control whether these
           files are reused (vs. destroyed). This function considers a package
           fully-installed if there is a DB entry for it (in that way, it is
           more strict than Package.installed). The return value is used to
           indicate when the prefix exists but the install is not complete.
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
            spack.stage_path)
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

        install(self.log_path, log_install_path)
        install(self.env_path, env_install_path)
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
            return join_path(self.stage.source_path, 'spack-build.out')

    @property
    def module(self):
        """Use this to add variables to the class's module's scope.
           This lets us use custom syntax in the install method.
        """
        return __import__(self.__class__.__module__,
                          fromlist=[self.__class__.__name__])

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

    def inject_flags(self, name, flags):
        """
        flag_handler that injects all flags through the compiler wrapper.
        """
        return (flags, None, None)

    def env_flags(self, name, flags):
        """
        flag_handler that adds all flags to canonical environment variables.
        """
        return (None, flags, None)

    def build_system_flags(self, name, flags):
        """
        flag_handler that passes flags to the build system arguments.  Any
        package using `build_system_flags` must also implement
        `flags_to_build_system_args`, or derive from a class that
        implements it.  Currently, AutotoolsPackage and CMakePackage
        implement it.
        """
        return (None, None, flags)

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
        except spack.repository.UnknownEntityError:
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

    def do_activate(self, with_dependencies=True, ignore_conflicts=False,
                    verbose=True, extensions_layout=None):
        """Called on an extension to invoke the extendee's activate method.

        Commands should call this routine, and should not call
        activate() directly.
        """
        if verbose:
            tty.msg("Activating extension %s for %s" %
                    (self.spec.cshort_spec, self.extendee_spec.cshort_spec))

        self._sanity_check_extension()

        if extensions_layout is None:
            extensions_layout = spack.store.extensions

        extensions_layout.check_extension_conflict(
            self.extendee_spec, self.spec)

        # Activate any package dependencies that are also extensions.
        if with_dependencies:
            for spec in self.dependency_activations():
                if not spec.package.is_activated(
                        extensions_layout=extensions_layout):
                    spec.package.do_activate(
                        with_dependencies=with_dependencies,
                        ignore_conflicts=ignore_conflicts,
                        verbose=verbose,
                        extensions_layout=extensions_layout)

        self.extendee_spec.package.activate(
            self, extensions_layout=extensions_layout,
            ignore_conflicts=ignore_conflicts, **self.extendee_args)

        extensions_layout.add_extension(self.extendee_spec, self.spec)

        if verbose:
            tty.msg(
                "Activated extension %s for %s" %
                (self.spec.short_spec,
                 self.extendee_spec.cformat("$_$@$+$%@")))

    def dependency_activations(self):
        return (spec for spec in self.spec.traverse(root=False, deptype='run')
                if spec.package.extends(self.extendee_spec))

    def activate(self, extension, ignore_conflicts=False, **kwargs):
        """Make extension package usable by linking all its files to a target
        provided by the directory layout (depending if the user wants to
        activate globally or in a specified file system view).

        Package authors can override this method to support other
        extension mechanisms.  Spack internals (commands, hooks, etc.)
        should call do_activate() method so that proper checks are
        always executed.

        """
        extensions_layout = kwargs.get("extensions_layout",
                                       spack.store.extensions)
        target = extensions_layout.extendee_target_directory(self)

        def ignore(filename):
            return (filename in spack.store.layout.hidden_file_paths or
                    kwargs.get('ignore', lambda f: False)(filename))

        tree = LinkTree(extension.prefix)

        conflict = tree.find_conflict(target, ignore=ignore)
        if not conflict:
            pass
        elif ignore_conflicts:
            tty.warn("While activating %s, found conflict %s" %
                     (self.spec.cshort_spec, conflict))
        else:
            raise ExtensionConflictError(conflict)

        tree.merge(target, ignore=ignore, link=extensions_layout.link,
                   ignore_conflicts=ignore_conflicts)

    def do_deactivate(self, **kwargs):
        """Called on the extension to invoke extendee's deactivate() method.

        `remove_dependents=True` deactivates extensions depending on this
        package instead of raising an error.
        """
        self._sanity_check_extension()
        force = kwargs.get('force', False)
        verbose = kwargs.get("verbose", True)
        remove_dependents = kwargs.get("remove_dependents", False)
        extensions_layout = kwargs.get("extensions_layout",
                                       spack.store.extensions)

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
                            msg = ("Cannot deactivate %s because %s is "
                                   "activated and depends on it.")
                            raise ActivationError(
                                msg % (self.spec.cshort_spec,
                                       aspec.cshort_spec))

        self.extendee_spec.package.deactivate(
            self,
            extensions_layout=extensions_layout,
            **self.extendee_args)

        # redundant activation check -- makes SURE the spec is not
        # still activated even if something was wrong above.
        if self.is_activated(extensions_layout):
            extensions_layout.remove_extension(
                self.extendee_spec, self.spec)

        if verbose:
            tty.msg(
                "Deactivated extension %s for %s" %
                (self.spec.short_spec,
                 self.extendee_spec.cformat("$_$@$+$%@")))

    def deactivate(self, extension, **kwargs):
        """Unlinks all files from extension out of this package's install dir
        or the corresponding filesystem view.

        Package authors can override this method to support other
        extension mechanisms.  Spack internals (commands, hooks, etc.)
        should call do_deactivate() method so that proper checks are
        always executed.

        """
        extensions_layout = kwargs.get("extensions_layout",
                                       spack.store.extensions)
        target = extensions_layout.extendee_target_directory(self)

        def ignore(filename):
            return (filename in spack.store.layout.hidden_file_paths or
                    kwargs.get('ignore', lambda f: False)(filename))

        tree = LinkTree(extension.prefix)
        tree.unmerge(target, ignore=ignore)

    def do_restage(self):
        """Reverts expanded/checked out source to a pristine state."""
        self.stage.restage()

    def do_clean(self):
        """Removes the package's build stage and source tarball."""
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
        urls = []
        if self.url:
            urls.append(self.url)

        for args in self.versions.values():
            if 'url' in args:
                urls.append(args['url'])
        return urls

    def fetch_remote_versions(self):
        """Try to find remote versions of this package using the
           list_url and any other URLs described in the package file."""
        if not self.all_urls:
            raise spack.util.web.VersionFetchError(self.__class__)

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
            source_repo_root = join_path(source, node.namespace)

            # There's no provenance installed for the source package.  Skip it.
            # User can always get something current from the builtin repo.
            if not os.path.isdir(source_repo_root):
                continue

            # Create a source repo and get the pkg directory out of it.
            try:
                source_repo = spack.repository.Repo(source_repo_root)
                source_pkg_dir = source_repo.dirname_for_package_name(
                    node.name)
            except spack.repository.RepoError:
                tty.warn("Warning: Couldn't copy in provenance for %s" %
                         node.name)

        # Create a destination repository
        dest_repo_root = join_path(path, node.namespace)
        if not os.path.exists(dest_repo_root):
            spack.repository.create_repo(dest_repo_root)
        repo = spack.repository.Repo(dest_repo_root)

        # Get the location of the package in the dest repo.
        dest_pkg_dir = repo.dirname_for_package_name(node.name)
        if os.path.exists(dest_pkg_dir):
            continue

        if node is not spec:
            install_tree(source_pkg_dir, dest_pkg_dir)
        else:
            spack.repo.dump_provenance(node, dest_pkg_dir)


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

    pass


class ExtensionConflictError(ExtensionError):

    def __init__(self, path):
        super(ExtensionConflictError, self).__init__(
            "Extension blocked by file: %s" % path)


class ActivationError(ExtensionError):

    def __init__(self, msg, long_msg=None):
        super(ActivationError, self).__init__(msg, long_msg)


class DependencyConflictError(spack.error.SpackError):
    """Raised when the dependencies cannot be flattened as asked for."""

    def __init__(self, conflict):
        super(DependencyConflictError, self).__init__(
            "%s conflicts with another file in the flattened directory." % (
                conflict))
