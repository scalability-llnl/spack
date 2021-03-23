# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module contains all routines related to setting up the package
build environment.  All of this is set up by package.py just before
install() is called.

There are two parts to the build environment:

1. Python build environment (i.e. install() method)

   This is how things are set up when install() is called.  Spack
   takes advantage of each package being in its own module by adding a
   bunch of command-like functions (like configure(), make(), etc.) in
   the package's module scope.  Ths allows package writers to call
   them all directly in Package.install() without writing 'self.'
   everywhere.  No, this isn't Pythonic.  Yes, it makes the code more
   readable and more like the shell script from which someone is
   likely porting.

2. Build execution environment

   This is the set of environment variables, like PATH, CC, CXX,
   etc. that control the build.  There are also a number of
   environment variables used to pass information (like RPATHs and
   other information about dependencies) to Spack's compiler wrappers.
   All of these env vars are also set up here.

Skimming this module is a nice way to get acquainted with the types of
calls you can make from within the install() function.
"""
import inspect
import re
import multiprocessing
import os
import shutil
import sys
import traceback
import types
from six import StringIO

import llnl.util.tty as tty
from llnl.util.tty.color import cescape, colorize
from llnl.util.filesystem import mkdirp, install, install_tree
from llnl.util.lang import dedupe
from llnl.util.tty.log import MultiProcessFd

import spack.build_systems.cmake
import spack.build_systems.meson
import spack.config
import spack.main
import spack.paths
import spack.package
import spack.repo
import spack.schema.environment
import spack.store
import spack.install_test
import spack.subprocess_context
import spack.architecture as arch
import spack.util.path
from spack.util.string import plural
from spack.util.environment import (
    env_flag, filter_system_paths, get_path, is_system_path,
    EnvironmentModifications, validate, preserve_environment)
from spack.util.environment import system_dirs
from spack.error import NoLibrariesError, NoHeadersError
from spack.util.executable import Executable
from spack.util.module_cmd import load_module, path_from_modules, module
from spack.util.log_parse import parse_log_events, make_log_context


#
# This can be set by the user to globally disable parallel builds.
#
SPACK_NO_PARALLEL_MAKE = 'SPACK_NO_PARALLEL_MAKE'

#
# These environment variables are set by
# set_build_environment_variables and used to pass parameters to
# Spack's compiler wrappers.
#
SPACK_ENV_PATH = 'SPACK_ENV_PATH'
SPACK_INCLUDE_DIRS = 'SPACK_INCLUDE_DIRS'
SPACK_LINK_DIRS = 'SPACK_LINK_DIRS'
SPACK_RPATH_DIRS = 'SPACK_RPATH_DIRS'
SPACK_RPATH_DEPS = 'SPACK_RPATH_DEPS'
SPACK_LINK_DEPS = 'SPACK_LINK_DEPS'
SPACK_PREFIX = 'SPACK_PREFIX'
SPACK_INSTALL = 'SPACK_INSTALL'
SPACK_DEBUG = 'SPACK_DEBUG'
SPACK_SHORT_SPEC = 'SPACK_SHORT_SPEC'
SPACK_DEBUG_LOG_ID = 'SPACK_DEBUG_LOG_ID'
SPACK_DEBUG_LOG_DIR = 'SPACK_DEBUG_LOG_DIR'
SPACK_CCACHE_BINARY = 'SPACK_CCACHE_BINARY'
SPACK_SYSTEM_DIRS = 'SPACK_SYSTEM_DIRS'


# Platform-specific library suffix.
dso_suffix = 'dylib' if sys.platform == 'darwin' else 'so'


class MakeExecutable(Executable):
    """Special callable executable object for make so the user can specify
       parallelism options on a per-invocation basis.  Specifying
       'parallel' to the call will override whatever the package's
       global setting is, so you can either default to true or false and
       override particular calls. Specifying 'jobs_env' to a particular
       call will name an environment variable which will be set to the
       parallelism level (without affecting the normal invocation with
       -j).

       Note that if the SPACK_NO_PARALLEL_MAKE env var is set it overrides
       everything.
    """

    def __init__(self, name, jobs):
        super(MakeExecutable, self).__init__(name)
        self.jobs = jobs

    def __call__(self, *args, **kwargs):
        """parallel, and jobs_env from kwargs are swallowed and used here;
        remaining arguments are passed through to the superclass.
        """

        disable = env_flag(SPACK_NO_PARALLEL_MAKE)
        parallel = (not disable) and kwargs.pop('parallel', self.jobs > 1)

        if parallel:
            args = ('-j{0}'.format(self.jobs),) + args
            jobs_env = kwargs.pop('jobs_env', None)
            if jobs_env:
                # Caller wants us to set an environment variable to
                # control the parallelism.
                kwargs['extra_env'] = {jobs_env: str(self.jobs)}

        return super(MakeExecutable, self).__call__(*args, **kwargs)


def clean_environment():
    # Stuff in here sanitizes the build environment to eliminate
    # anything the user has set that may interfere. We apply it immediately
    # unlike the other functions so it doesn't overwrite what the modules load.
    env = EnvironmentModifications()

    # Remove these vars from the environment during build because they
    # can affect how some packages find libraries.  We want to make
    # sure that builds never pull in unintended external dependencies.
    env.unset('LD_LIBRARY_PATH')
    env.unset('LD_RUN_PATH')
    env.unset('DYLD_LIBRARY_PATH')
    env.unset('DYLD_FALLBACK_LIBRARY_PATH')

    # These vars affect how the compiler finds libraries and include dirs.
    env.unset('LIBRARY_PATH')
    env.unset('CPATH')
    env.unset('C_INCLUDE_PATH')
    env.unset('CPLUS_INCLUDE_PATH')
    env.unset('OBJC_INCLUDE_PATH')

    # On Cray "cluster" systems, unset CRAY_LD_LIBRARY_PATH to avoid
    # interference with Spack dependencies.
    # CNL requires these variables to be set (or at least some of them,
    # depending on the CNL version).
    hostarch = arch.Arch(arch.platform(), 'default_os', 'default_target')
    on_cray = str(hostarch.platform) == 'cray'
    using_cnl = re.match(r'cnl\d+', str(hostarch.os))
    if on_cray and not using_cnl:
        env.unset('CRAY_LD_LIBRARY_PATH')
        for varname in os.environ.keys():
            if 'PKGCONF' in varname:
                env.unset(varname)

    # Unset the following variables because they can affect installation of
    # Autotools and CMake packages.
    build_system_vars = [
        'CC', 'CFLAGS', 'CPP', 'CPPFLAGS',  # C variables
        'CXX', 'CCC', 'CXXFLAGS', 'CXXCPP',  # C++ variables
        'F77', 'FFLAGS', 'FLIBS',  # Fortran77 variables
        'FC', 'FCFLAGS', 'FCLIBS',  # Fortran variables
        'LDFLAGS', 'LIBS'  # linker variables
    ]
    for v in build_system_vars:
        env.unset(v)

    # Unset mpi environment vars. These flags should only be set by
    # mpi providers for packages with mpi dependencies
    mpi_vars = [
        'MPICC', 'MPICXX', 'MPIFC', 'MPIF77', 'MPIF90'
    ]
    for v in mpi_vars:
        env.unset(v)

    build_lang = spack.config.get('config:build_language')
    if build_lang:
        # Override language-related variables. This can be used to force
        # English compiler messages etc., which allows parse_log_events to
        # show useful matches.
        env.set('LC_ALL', build_lang)

    # Remove any macports installs from the PATH.  The macports ld can
    # cause conflicts with the built-in linker on el capitan.  Solves
    # assembler issues, e.g.:
    #    suffix or operands invalid for `movq'"
    path = get_path('PATH')
    for p in path:
        if '/macports/' in p:
            env.remove_path('PATH', p)

    env.apply_modifications()


def set_compiler_environment_variables(pkg, env):
    assert pkg.spec.concrete
    compiler = pkg.compiler
    spec = pkg.spec

    # Make sure the executables for this compiler exist
    compiler.verify_executables()

    # Set compiler variables used by CMake and autotools
    assert all(key in compiler.link_paths for key in (
        'cc', 'cxx', 'f77', 'fc'))

    # Populate an object with the list of environment modifications
    # and return it
    # TODO : add additional kwargs for better diagnostics, like requestor,
    # ttyout, ttyerr, etc.
    link_dir = spack.paths.build_env_path

    # Set SPACK compiler variables so that our wrapper knows what to call
    if compiler.cc:
        env.set('SPACK_CC', compiler.cc)
        env.set('CC', os.path.join(link_dir, compiler.link_paths['cc']))
    if compiler.cxx:
        env.set('SPACK_CXX', compiler.cxx)
        env.set('CXX', os.path.join(link_dir, compiler.link_paths['cxx']))
    if compiler.f77:
        env.set('SPACK_F77', compiler.f77)
        env.set('F77', os.path.join(link_dir, compiler.link_paths['f77']))
    if compiler.fc:
        env.set('SPACK_FC',  compiler.fc)
        env.set('FC', os.path.join(link_dir, compiler.link_paths['fc']))

    # Set SPACK compiler rpath flags so that our wrapper knows what to use
    env.set('SPACK_CC_RPATH_ARG',  compiler.cc_rpath_arg)
    env.set('SPACK_CXX_RPATH_ARG', compiler.cxx_rpath_arg)
    env.set('SPACK_F77_RPATH_ARG', compiler.f77_rpath_arg)
    env.set('SPACK_FC_RPATH_ARG',  compiler.fc_rpath_arg)
    env.set('SPACK_LINKER_ARG', compiler.linker_arg)

    # Check whether we want to force RPATH or RUNPATH
    if spack.config.get('config:shared_linking') == 'rpath':
        env.set('SPACK_DTAGS_TO_STRIP', compiler.enable_new_dtags)
        env.set('SPACK_DTAGS_TO_ADD', compiler.disable_new_dtags)
    else:
        env.set('SPACK_DTAGS_TO_STRIP', compiler.disable_new_dtags)
        env.set('SPACK_DTAGS_TO_ADD', compiler.enable_new_dtags)

    # Set the target parameters that the compiler will add
    isa_arg = spec.architecture.target.optimization_flags(compiler)
    env.set('SPACK_TARGET_ARGS', isa_arg)

    # Trap spack-tracked compiler flags as appropriate.
    # env_flags are easy to accidentally override.
    inject_flags = {}
    env_flags = {}
    build_system_flags = {}
    for flag in spack.spec.FlagMap.valid_compiler_flags():
        # Always convert flag_handler to function type.
        # This avoids discrepencies in calling conventions between functions
        # and methods, or between bound and unbound methods in python 2.
        # We cannot effectively convert everything to a bound method, which
        # would be the simpler solution.
        if isinstance(pkg.flag_handler, types.FunctionType):
            handler = pkg.flag_handler
        else:
            if sys.version_info >= (3, 0):
                handler = pkg.flag_handler.__func__
            else:
                handler = pkg.flag_handler.im_func
        injf, envf, bsf = handler(pkg, flag, spec.compiler_flags[flag])
        inject_flags[flag] = injf or []
        env_flags[flag] = envf or []
        build_system_flags[flag] = bsf or []

    # Place compiler flags as specified by flag_handler
    for flag in spack.spec.FlagMap.valid_compiler_flags():
        # Concreteness guarantees key safety here
        if inject_flags[flag]:
            # variables SPACK_<FLAG> inject flags through wrapper
            var_name = 'SPACK_{0}'.format(flag.upper())
            env.set(var_name, ' '.join(f for f in inject_flags[flag]))
        if env_flags[flag]:
            # implicit variables
            env.set(flag.upper(), ' '.join(f for f in env_flags[flag]))
    pkg.flags_to_build_system_args(build_system_flags)

    env.set('SPACK_COMPILER_SPEC', str(spec.compiler))

    env.set('SPACK_SYSTEM_DIRS', ':'.join(system_dirs))

    compiler.setup_custom_environment(pkg, env)

    return env


def set_build_environment_variables(pkg, env, dirty):
    """Ensure a clean install environment when we build packages.

    This involves unsetting pesky environment variables that may
    affect the build. It also involves setting environment variables
    used by Spack's compiler wrappers.

    Args:
        pkg: The package we are building
        env: The build environment
        dirty (bool): Skip unsetting the user's environment settings
    """
    # Gather information about various types of dependencies
    build_deps      = set(pkg.spec.dependencies(deptype=('build', 'test')))
    link_deps       = set(pkg.spec.traverse(root=False, deptype=('link')))
    build_link_deps = build_deps | link_deps
    rpath_deps      = get_rpath_deps(pkg)

    link_dirs = []
    include_dirs = []
    rpath_dirs = []

    # The top-level package is always RPATHed. It hasn't been installed yet
    # so the RPATHs are added unconditionally (e.g. even though lib64/ may
    # not be created for the install).
    for libdir in ['lib', 'lib64']:
        lib_path = os.path.join(pkg.prefix, libdir)
        rpath_dirs.append(lib_path)

    # Set up link, include, RPATH directories that are passed to the
    # compiler wrapper
    for dep in link_deps:
        if is_system_path(dep.prefix):
            continue
        query = pkg.spec[dep.name]
        dep_link_dirs = list()
        try:
            dep_link_dirs.extend(query.libs.directories)
        except NoLibrariesError:
            tty.debug("No libraries found for {0}".format(dep.name))

        for default_lib_dir in ['lib', 'lib64']:
            default_lib_prefix = os.path.join(dep.prefix, default_lib_dir)
            if os.path.isdir(default_lib_prefix):
                dep_link_dirs.append(default_lib_prefix)

        link_dirs.extend(dep_link_dirs)
        if dep in rpath_deps:
            rpath_dirs.extend(dep_link_dirs)

        try:
            include_dirs.extend(query.headers.directories)
        except NoHeadersError:
            tty.debug("No headers found for {0}".format(dep.name))

    link_dirs = list(dedupe(filter_system_paths(link_dirs)))
    include_dirs = list(dedupe(filter_system_paths(include_dirs)))
    rpath_dirs = list(dedupe(filter_system_paths(rpath_dirs)))

    env.set(SPACK_LINK_DIRS, ':'.join(link_dirs))
    env.set(SPACK_INCLUDE_DIRS, ':'.join(include_dirs))
    env.set(SPACK_RPATH_DIRS, ':'.join(rpath_dirs))

    build_prefixes      = [dep.prefix for dep in build_deps]
    build_link_prefixes = [dep.prefix for dep in build_link_deps]

    # add run-time dependencies of direct build-time dependencies:
    for build_dep in build_deps:
        for run_dep in build_dep.traverse(deptype='run'):
            build_prefixes.append(run_dep.prefix)

    # Filter out system paths: ['/', '/usr', '/usr/local']
    # These paths can be introduced into the build when an external package
    # is added as a dependency. The problem with these paths is that they often
    # contain hundreds of other packages installed in the same directory.
    # If these paths come first, they can overshadow Spack installations.
    build_prefixes      = filter_system_paths(build_prefixes)
    build_link_prefixes = filter_system_paths(build_link_prefixes)

    # Add dependencies to CMAKE_PREFIX_PATH
    env.set_path('CMAKE_PREFIX_PATH', build_link_prefixes)

    # Set environment variables if specified for
    # the given compiler
    compiler = pkg.compiler
    env.extend(spack.schema.environment.parse(compiler.environment))

    if compiler.extra_rpaths:
        extra_rpaths = ':'.join(compiler.extra_rpaths)
        env.set('SPACK_COMPILER_EXTRA_RPATHS', extra_rpaths)

    # Add bin directories from dependencies to the PATH for the build.
    for prefix in build_prefixes:
        for dirname in ['bin', 'bin64']:
            bin_dir = os.path.join(prefix, dirname)
            if os.path.isdir(bin_dir):
                env.prepend_path('PATH', bin_dir)

    # Add spack build environment path with compiler wrappers first in
    # the path. We add the compiler wrapper path, which includes default
    # wrappers (cc, c++, f77, f90), AND a subdirectory containing
    # compiler-specific symlinks.  The latter ensures that builds that
    # are sensitive to the *name* of the compiler see the right name when
    # we're building with the wrappers.
    #
    # Conflicts on case-insensitive systems (like "CC" and "cc") are
    # handled by putting one in the <build_env_path>/case-insensitive
    # directory.  Add that to the path too.
    env_paths = []
    compiler_specific = os.path.join(
        spack.paths.build_env_path, os.path.dirname(pkg.compiler.link_paths['cc']))
    for item in [spack.paths.build_env_path, compiler_specific]:
        env_paths.append(item)
        ci = os.path.join(item, 'case-insensitive')
        if os.path.isdir(ci):
            env_paths.append(ci)

    for item in env_paths:
        env.prepend_path('PATH', item)
    env.set_path(SPACK_ENV_PATH, env_paths)

    # Working directory for the spack command itself, for debug logs.
    if spack.config.get('config:debug'):
        env.set(SPACK_DEBUG, 'TRUE')
    env.set(SPACK_SHORT_SPEC, pkg.spec.short_spec)
    env.set(SPACK_DEBUG_LOG_ID, pkg.spec.format('{name}-{hash:7}'))
    env.set(SPACK_DEBUG_LOG_DIR, spack.main.spack_working_dir)

    # Find ccache binary and hand it to build environment
    if spack.config.get('config:ccache'):
        ccache = Executable('ccache')
        if not ccache:
            raise RuntimeError("No ccache binary found in PATH")
        env.set(SPACK_CCACHE_BINARY, ccache)

    # Add any pkgconfig directories to PKG_CONFIG_PATH
    for prefix in build_link_prefixes:
        for directory in ('lib', 'lib64', 'share'):
            pcdir = os.path.join(prefix, directory, 'pkgconfig')
            if os.path.isdir(pcdir):
                env.prepend_path('PKG_CONFIG_PATH', pcdir)

    return env


def _set_variables_for_single_module(pkg, module):
    """Helper function to set module variables for single module."""
    # Put a marker on this module so that it won't execute the body of this
    # function again, since it is not needed
    marker = '_set_run_already_called'
    if getattr(module, marker, False):
        return

    jobs = spack.config.get('config:build_jobs', 16) if pkg.parallel else 1
    jobs = min(jobs, multiprocessing.cpu_count())

    m = module
    m.make_jobs = jobs

    # TODO: make these build deps that can be installed if not found.
    m.make = MakeExecutable('make', jobs)
    m.gmake = MakeExecutable('gmake', jobs)
    m.scons = MakeExecutable('scons', jobs)
    m.ninja = MakeExecutable('ninja', jobs)

    # easy shortcut to os.environ
    m.env = os.environ

    # Find the configure script in the archive path
    # Don't use which for this; we want to find it in the current dir.
    m.configure = Executable('./configure')

    m.meson = Executable('meson')
    m.cmake = Executable('cmake')
    m.ctest = MakeExecutable('ctest', jobs)

    # Standard CMake arguments
    m.std_cmake_args = spack.build_systems.cmake.CMakePackage._std_args(pkg)
    m.std_meson_args = spack.build_systems.meson.MesonPackage._std_args(pkg)

    # Put spack compiler paths in module scope.
    link_dir = spack.paths.build_env_path
    m.spack_cc = os.path.join(link_dir, pkg.compiler.link_paths['cc'])
    m.spack_cxx = os.path.join(link_dir, pkg.compiler.link_paths['cxx'])
    m.spack_f77 = os.path.join(link_dir, pkg.compiler.link_paths['f77'])
    m.spack_fc = os.path.join(link_dir, pkg.compiler.link_paths['fc'])

    # Emulate some shell commands for convenience
    m.pwd = os.getcwd
    m.cd = os.chdir
    m.mkdir = os.mkdir
    m.makedirs = os.makedirs
    m.remove = os.remove
    m.removedirs = os.removedirs
    m.symlink = os.symlink

    m.mkdirp = mkdirp
    m.install = install
    m.install_tree = install_tree
    m.rmtree = shutil.rmtree
    m.move = shutil.move

    # Useful directories within the prefix are encapsulated in
    # a Prefix object.
    m.prefix = pkg.prefix

    # Platform-specific library suffix.
    m.dso_suffix = dso_suffix

    def static_to_shared_library(static_lib, shared_lib=None, **kwargs):
        compiler_path = kwargs.get('compiler', m.spack_cc)
        compiler = Executable(compiler_path)

        return _static_to_shared_library(pkg.spec.architecture, compiler,
                                         static_lib, shared_lib, **kwargs)

    m.static_to_shared_library = static_to_shared_library

    # Put a marker on this module so that it won't execute the body of this
    # function again, since it is not needed
    setattr(m, marker, True)


def set_module_variables_for_package(pkg):
    """Populate the module scope of install() with some useful functions.
       This makes things easier for package writers.
    """
    # If a user makes their own package repo, e.g.
    # spack.pkg.mystuff.libelf.Libelf, and they inherit from an existing class
    # like spack.pkg.original.libelf.Libelf, then set the module variables
    # for both classes so the parent class can still use them if it gets
    # called. parent_class_modules includes pkg.module.
    modules = parent_class_modules(pkg.__class__)
    for mod in modules:
        _set_variables_for_single_module(pkg, mod)


def _static_to_shared_library(arch, compiler, static_lib, shared_lib=None,
                              **kwargs):
    """
    Converts a static library to a shared library. The static library has to
    be built with PIC for the conversion to work.

    Parameters:
        static_lib (str): Path to the static library.
        shared_lib (str): Path to the shared library. Default is to derive
                          from the static library's path.

    Keyword arguments:
        compiler (str): Path to the compiler. Default is spack_cc.
        compiler_output: Where to print compiler output to.
        arguments (str list): Additional arguments for the compiler.
        version (str): Library version. Default is unspecified.
        compat_version (str): Library compatibility version. Default is
                              version.
    """
    compiler_output = kwargs.get('compiler_output', None)
    arguments = kwargs.get('arguments', [])
    version = kwargs.get('version', None)
    compat_version = kwargs.get('compat_version', version)

    if not shared_lib:
        shared_lib = '{0}.{1}'.format(os.path.splitext(static_lib)[0],
                                      dso_suffix)

    compiler_args = []

    # TODO: Compiler arguments should not be hardcoded but provided by
    #       the different compiler classes.
    if 'linux' in arch or 'cray' in arch:
        soname = os.path.basename(shared_lib)

        if compat_version:
            soname += '.{0}'.format(compat_version)

        compiler_args = [
            '-shared',
            '-Wl,-soname,{0}'.format(soname),
            '-Wl,--whole-archive',
            static_lib,
            '-Wl,--no-whole-archive'
        ]
    elif 'darwin' in arch:
        install_name = shared_lib

        if compat_version:
            install_name += '.{0}'.format(compat_version)

        compiler_args = [
            '-dynamiclib',
            '-install_name', '{0}'.format(install_name),
            '-Wl,-force_load,{0}'.format(static_lib)
        ]

        if compat_version:
            compiler_args.extend(['-compatibility_version', '{0}'.format(
                compat_version)])

        if version:
            compiler_args.extend(['-current_version', '{0}'.format(version)])

    if len(arguments) > 0:
        compiler_args.extend(arguments)

    shared_lib_base = shared_lib

    if version:
        shared_lib += '.{0}'.format(version)
    elif compat_version:
        shared_lib += '.{0}'.format(compat_version)

    compiler_args.extend(['-o', shared_lib])

    # Create symlinks for version and compat_version
    shared_lib_link = os.path.basename(shared_lib)

    if version or compat_version:
        os.symlink(shared_lib_link, shared_lib_base)

    if compat_version and compat_version != version:
        os.symlink(shared_lib_link, '{0}.{1}'.format(shared_lib_base,
                                                     compat_version))

    return compiler(*compiler_args, output=compiler_output)


def get_rpath_deps(pkg):
    """Return immediate or transitive RPATHs depending on the package."""
    if pkg.transitive_rpaths:
        return [d for d in pkg.spec.traverse(root=False, deptype=('link'))]
    else:
        return pkg.spec.dependencies(deptype='link')


def get_rpaths(pkg):
    """Get a list of all the rpaths for a package."""
    rpaths = [pkg.prefix.lib, pkg.prefix.lib64]
    deps = get_rpath_deps(pkg)
    rpaths.extend(d.prefix.lib for d in deps
                  if os.path.isdir(d.prefix.lib))
    rpaths.extend(d.prefix.lib64 for d in deps
                  if os.path.isdir(d.prefix.lib64))
    # Second module is our compiler mod name. We use that to get rpaths from
    # module show output.
    if pkg.compiler.modules and len(pkg.compiler.modules) > 1:
        rpaths.append(path_from_modules([pkg.compiler.modules[1]]))
    return list(dedupe(filter_system_paths(rpaths)))


def get_std_cmake_args(pkg):
    """List of standard arguments used if a package is a CMakePackage.

    Returns:
        list of str: standard arguments that would be used if this
        package were a CMakePackage instance.

    Args:
        pkg (PackageBase): package under consideration

    Returns:
        list of str: arguments for cmake
    """
    return spack.build_systems.cmake.CMakePackage._std_args(pkg)


def get_std_meson_args(pkg):
    """List of standard arguments used if a package is a MesonPackage.

    Returns:
        list of str: standard arguments that would be used if this
        package were a MesonPackage instance.

    Args:
        pkg (PackageBase): package under consideration

    Returns:
        list of str: arguments for meson
    """
    return spack.build_systems.meson.MesonPackage._std_args(pkg)


def parent_class_modules(cls):
    """
    Get list of superclass modules that descend from spack.package.PackageBase

    Includes cls.__module__
    """
    if (not issubclass(cls, spack.package.PackageBase) or
        issubclass(spack.package.PackageBase, cls)):
        return []
    result = []
    module = sys.modules.get(cls.__module__)
    if module:
        result = [module]
    for c in cls.__bases__:
        result.extend(parent_class_modules(c))
    return result


def load_external_modules(pkg):
    """Traverse a package's spec DAG and load any external modules.

    Traverse a package's dependencies and load any external modules
    associated with them.

    Args:
        pkg (PackageBase): package to load deps for
    """
    for dep in list(pkg.spec.traverse()):
        external_modules = dep.external_modules or []
        for external_module in external_modules:
            load_module(external_module)


def setup_package(pkg, dirty, context='build'):
    """Execute all environment setup routines."""
    env = EnvironmentModifications()

    if not dirty:
        clean_environment()

    # setup compilers and build tools for build contexts
    need_compiler = context == 'build' or (context == 'test' and
                                           pkg.test_requires_compiler)
    if need_compiler:
        set_compiler_environment_variables(pkg, env)
        set_build_environment_variables(pkg, env, dirty)

    # architecture specific setup
    pkg.architecture.platform.setup_platform_environment(pkg, env)

    if context == 'build':
        # recursive post-order dependency information
        env.extend(
            modifications_from_dependencies(pkg.spec, context=context)
        )

        if (not dirty) and (not env.is_unset('CPATH')):
            tty.debug("A dependency has updated CPATH, this may lead pkg-"
                      "config to assume that the package is part of the system"
                      " includes and omit it when invoked with '--cflags'.")

        # setup package itself
        set_module_variables_for_package(pkg)
        pkg.setup_build_environment(env)
    elif context == 'test':
        import spack.user_environment as uenv  # avoid circular import
        env.extend(uenv.environment_modifications_for_spec(pkg.spec))
        env.extend(
            modifications_from_dependencies(pkg.spec, context=context)
        )
        set_module_variables_for_package(pkg)
        env.prepend_path('PATH', '.')

    # Loading modules, in particular if they are meant to be used outside
    # of Spack, can change environment variables that are relevant to the
    # build of packages. To avoid a polluted environment, preserve the
    # value of a few, selected, environment variables
    # With the current ordering of environment modifications, this is strictly
    # unnecessary. Modules affecting these variables will be overwritten anyway
    with preserve_environment('CC', 'CXX', 'FC', 'F77'):
        # All module loads that otherwise would belong in previous
        # functions have to occur after the env object has its
        # modifications applied. Otherwise the environment modifications
        # could undo module changes, such as unsetting LD_LIBRARY_PATH
        # after a module changes it.
        if need_compiler:
            for mod in pkg.compiler.modules:
                # Fixes issue https://github.com/spack/spack/issues/3153
                if os.environ.get("CRAY_CPU_TARGET") == "mic-knl":
                    load_module("cce")
                load_module(mod)

        # kludge to handle cray libsci being automatically loaded by PrgEnv
        # modules on cray platform. Module unload does no damage when
        # unnecessary
        module('unload', 'cray-libsci')

        if pkg.architecture.target.module_name:
            load_module(pkg.architecture.target.module_name)

        load_external_modules(pkg)

    implicit_rpaths = pkg.compiler.implicit_rpaths()
    if implicit_rpaths:
        env.set('SPACK_COMPILER_IMPLICIT_RPATHS',
                ':'.join(implicit_rpaths))

    # Make sure nothing's strange about the Spack environment.
    validate(env, tty.warn)
    env.apply_modifications()


def modifications_from_dependencies(spec, context):
    """Returns the environment modifications that are required by
    the dependencies of a spec and also applies modifications
    to this spec's package at module scope, if need be.

    Args:
        spec (Spec): spec for which we want the modifications
        context (str): either 'build' for build-time modifications or 'run'
            for run-time modifications
    """
    env = EnvironmentModifications()
    pkg = spec.package

    # Maps the context to deptype and method to be called
    deptype_and_method = {
        'build': (('build', 'link', 'test'),
                  'setup_dependent_build_environment'),
        'run': (('link', 'run'), 'setup_dependent_run_environment'),
        'test': (('link', 'run', 'test'), 'setup_dependent_run_environment')
    }
    deptype, method = deptype_and_method[context]

    root = context == 'test'
    for dspec in spec.traverse(order='post', root=root, deptype=deptype):
        dpkg = dspec.package
        set_module_variables_for_package(dpkg)
        # Allow dependencies to modify the module
        dpkg.setup_dependent_package(pkg.module, spec)
        getattr(dpkg, method)(env, spec)

    return env


def _setup_pkg_and_run(serialized_pkg, function, kwargs, child_pipe,
                       input_multiprocess_fd):

    context = kwargs.get('context', 'build')

    try:
        # We are in the child process. Python sets sys.stdin to
        # open(os.devnull) to prevent our process and its parent from
        # simultaneously reading from the original stdin. But, we assume
        # that the parent process is not going to read from it till we
        # are done with the child, so we undo Python's precaution.
        if input_multiprocess_fd is not None:
            sys.stdin = os.fdopen(input_multiprocess_fd.fd)

        pkg = serialized_pkg.restore()

        if not kwargs.get('fake', False):
            kwargs['unmodified_env'] = os.environ.copy()
            setup_package(pkg, dirty=kwargs.get('dirty', False),
                          context=context)
        return_value = function(pkg, kwargs)
        child_pipe.send(return_value)

    except StopPhase as e:
        # Do not create a full ChildError from this, it's not an error
        # it's a control statement.
        child_pipe.send(e)
    except BaseException:
        # catch ANYTHING that goes wrong in the child process
        exc_type, exc, tb = sys.exc_info()

        # Need to unwind the traceback in the child because traceback
        # objects can't be sent to the parent.
        tb_string = traceback.format_exc()

        # build up some context from the offending package so we can
        # show that, too.
        package_context = get_package_context(tb)

        logfile = None
        if context == 'build':
            try:
                if hasattr(pkg, 'log_path'):
                    logfile = pkg.log_path
            except NameError:
                # 'pkg' is not defined yet
                pass
        elif context == 'test':
            logfile = os.path.join(
                pkg.test_suite.stage,
                spack.install_test.TestSuite.test_log_name(pkg.spec))

        # make a pickleable exception to send to parent.
        msg = "%s: %s" % (exc_type.__name__, str(exc))

        ce = ChildError(msg,
                        exc_type.__module__,
                        exc_type.__name__,
                        tb_string, logfile, context, package_context)
        child_pipe.send(ce)

    finally:
        child_pipe.close()
        if input_multiprocess_fd is not None:
            input_multiprocess_fd.close()


def start_build_process(pkg, function, kwargs):
    """Create a child process to do part of a spack build.

    Args:

        pkg (PackageBase): package whose environment we should set up the
            child process for.
        function (callable): argless function to run in the child
            process.

    Usage::

        def child_fun():
            # do stuff
        build_env.start_build_process(pkg, child_fun)

    The child process is run with the build environment set up by
    spack.build_environment.  This allows package authors to have full
    control over the environment, etc. without affecting other builds
    that might be executed in the same spack call.

    If something goes wrong, the child process catches the error and
    passes it to the parent wrapped in a ChildError.  The parent is
    expected to handle (or re-raise) the ChildError.

    This uses `multiprocessing.Process` to create the child process. The
    mechanism used to create the process differs on different operating
    systems and for different versions of Python. In some cases "fork"
    is used (i.e. the "fork" system call) and some cases it starts an
    entirely new Python interpreter process (in the docs this is referred
    to as the "spawn" start method). Breaking it down by OS:

    - Linux always uses fork.
    - Mac OS uses fork before Python 3.8 and "spawn" for 3.8 and after.
    - Windows always uses the "spawn" start method.

    For more information on `multiprocessing` child process creation
    mechanisms, see https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods
    """
    parent_pipe, child_pipe = multiprocessing.Pipe()
    input_multiprocess_fd = None

    serialized_pkg = spack.subprocess_context.PackageInstallContext(pkg)

    try:
        # Forward sys.stdin when appropriate, to allow toggling verbosity
        if sys.stdin.isatty() and hasattr(sys.stdin, 'fileno'):
            input_fd = os.dup(sys.stdin.fileno())
            input_multiprocess_fd = MultiProcessFd(input_fd)

        p = multiprocessing.Process(
            target=_setup_pkg_and_run,
            args=(serialized_pkg, function, kwargs, child_pipe,
                  input_multiprocess_fd))
        p.start()

    except InstallError as e:
        e.pkg = pkg
        raise

    finally:
        # Close the input stream in the parent process
        if input_multiprocess_fd is not None:
            input_multiprocess_fd.close()

    child_result = parent_pipe.recv()
    p.join()

    # If returns a StopPhase, raise it
    if isinstance(child_result, StopPhase):
        # do not print
        raise child_result

    # let the caller know which package went wrong.
    if isinstance(child_result, InstallError):
        child_result.pkg = pkg

    if isinstance(child_result, ChildError):
        # If the child process raised an error, print its output here rather
        # than waiting until the call to SpackError.die() in main(). This
        # allows exception handling output to be logged from within Spack.
        # see spack.main.SpackCommand.
        child_result.print_context()
        raise child_result

    return child_result


def get_package_context(traceback, context=3):
    """Return some context for an error message when the build fails.

    Args:
        traceback (traceback): A traceback from some exception raised during
            install

        context (int): Lines of context to show before and after the line
            where the error happened

    This function inspects the stack to find where we failed in the
    package file, and it adds detailed context to the long_message
    from there.

    """
    def make_stack(tb, stack=None):
        """Tracebacks come out of the system in caller -> callee order.  Return
        an array in callee -> caller order so we can traverse it."""
        if stack is None:
            stack = []
        if tb is not None:
            make_stack(tb.tb_next, stack)
            stack.append(tb)
        return stack

    stack = make_stack(traceback)

    for tb in stack:
        frame = tb.tb_frame
        if 'self' in frame.f_locals:
            # Find the first proper subclass of PackageBase.
            obj = frame.f_locals['self']
            if isinstance(obj, spack.package.PackageBase):
                break

    # We found obj, the Package implementation we care about.
    # Point out the location in the install method where we failed.
    lines = [
        '{0}:{1:d}, in {2}:'.format(
            inspect.getfile(frame.f_code),
            frame.f_lineno - 1,  # subtract 1 because f_lineno is 0-indexed
            frame.f_code.co_name
        )
    ]

    # Build a message showing context in the install method.
    sourcelines, start = inspect.getsourcelines(frame)

    # Calculate lineno of the error relative to the start of the function.
    # Subtract 1 because f_lineno is 0-indexed.
    fun_lineno = frame.f_lineno - start - 1
    start_ctx = max(0, fun_lineno - context)
    sourcelines = sourcelines[start_ctx:fun_lineno + context + 1]

    for i, line in enumerate(sourcelines):
        is_error = start_ctx + i == fun_lineno
        mark = '>> ' if is_error else '   '
        # Add start to get lineno relative to start of file, not function.
        marked = '  {0}{1:-6d}{2}'.format(
            mark, start + start_ctx + i, line.rstrip())
        if is_error:
            marked = colorize('@R{%s}' % cescape(marked))
        lines.append(marked)

    return lines


class InstallError(spack.error.SpackError):
    """Raised by packages when a package fails to install.

    Any subclass of InstallError will be annotated by Spack wtih a
    ``pkg`` attribute on failure, which the caller can use to get the
    package for which the exception was raised.
    """


class ChildError(InstallError):
    """Special exception class for wrapping exceptions from child processes
       in Spack's build environment.

    The main features of a ChildError are:

    1. They're serializable, so when a child build fails, we can send one
       of these to the parent and let the parent report what happened.

    2. They have a ``traceback`` field containing a traceback generated
       on the child immediately after failure.  Spack will print this on
       failure in lieu of trying to run sys.excepthook on the parent
       process, so users will see the correct stack trace from a child.

    3. They also contain context, which shows context in the Package
       implementation where the error happened.  This helps people debug
       Python code in their packages.  To get it, Spack searches the
       stack trace for the deepest frame where ``self`` is in scope and
       is an instance of PackageBase.  This will generally find a useful
       spot in the ``package.py`` file.

    The long_message of a ChildError displays one of two things:

      1. If the original error was a ProcessError, indicating a command
         died during the build, we'll show context from the build log.

      2. If the original error was any other type of error, we'll show
         context from the Python code.

    SpackError handles displaying the special traceback if we're in debug
    mode with spack -d.

    """
    # List of errors considered "build errors", for which we'll show log
    # context instead of Python context.
    build_errors = [('spack.util.executable', 'ProcessError')]

    def __init__(self, msg, module, classname, traceback_string, log_name,
                 log_type, context):
        super(ChildError, self).__init__(msg)
        self.module = module
        self.name = classname
        self.traceback = traceback_string
        self.log_name = log_name
        self.log_type = log_type
        self.context = context

    @property
    def long_message(self):
        out = StringIO()
        out.write(self._long_message if self._long_message else '')

        have_log = self.log_name and os.path.exists(self.log_name)

        if (self.module, self.name) in ChildError.build_errors:
            # The error happened in some external executed process. Show
            # the log with errors or warnings highlighted.
            if have_log:
                write_log_summary(out, self.log_type, self.log_name)

        else:
            # The error happened in the Python code, so try to show
            # some context from the Package itself.
            if self.context:
                out.write('\n')
                out.write('\n'.join(self.context))
                out.write('\n')

        if out.getvalue():
            out.write('\n')

        if have_log:
            out.write('See {0} log for details:\n'.format(self.log_type))
            out.write('  {0}\n'.format(self.log_name))

        return out.getvalue()

    def __str__(self):
        return self.message

    def __reduce__(self):
        """__reduce__ is used to serialize (pickle) ChildErrors.

        Return a function to reconstruct a ChildError, along with the
        salient properties we'll need.
        """
        return _make_child_error, (
            self.message,
            self.module,
            self.name,
            self.traceback,
            self.log_name,
            self.log_type,
            self.context)


def _make_child_error(msg, module, name, traceback, log, log_type, context):
    """Used by __reduce__ in ChildError to reconstruct pickled errors."""
    return ChildError(msg, module, name, traceback, log, log_type, context)


class StopPhase(spack.error.SpackError):
    """Pickle-able exception to control stopped builds."""
    def __reduce__(self):
        return _make_stop_phase, (self.message, self.long_message)


def _make_stop_phase(msg, long_msg):
    return StopPhase(msg, long_msg)


def write_log_summary(out, log_type, log, last=None):
    errors, warnings = parse_log_events(log)
    nerr = len(errors)
    nwar = len(warnings)

    if nerr > 0:
        if last and nerr > last:
            errors = errors[-last:]
            nerr = last

        # If errors are found, only display errors
        out.write(
            "\n%s found in %s log:\n" %
            (plural(nerr, 'error'), log_type))
        out.write(make_log_context(errors))
    elif nwar > 0:
        if last and nwar > last:
            warnings = warnings[-last:]
            nwar = last

        # If no errors are found but warnings are, display warnings
        out.write(
            "\n%s found in %s log:\n" %
            (plural(nwar, 'warning'), log_type))
        out.write(make_log_context(warnings))
