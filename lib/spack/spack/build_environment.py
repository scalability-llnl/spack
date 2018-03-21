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
import multiprocessing
import os
import shutil
import sys
import traceback
import types
from six import iteritems
from six import StringIO

import llnl.util.tty as tty
from llnl.util.tty.color import colorize
from llnl.util.filesystem import join_path, mkdirp, install, install_tree

import spack
import spack.store
from spack.environment import EnvironmentModifications, validate
from spack.util.environment import env_flag, filter_system_paths, get_path
from spack.util.executable import Executable
from spack.util.module_cmd import load_module, get_path_from_module
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
SPACK_DEPENDENCIES = 'SPACK_DEPENDENCIES'
SPACK_RPATH_DEPS = 'SPACK_RPATH_DEPS'
SPACK_LINK_DEPS = 'SPACK_LINK_DEPS'
SPACK_PREFIX = 'SPACK_PREFIX'
SPACK_INSTALL = 'SPACK_INSTALL'
SPACK_DEBUG = 'SPACK_DEBUG'
SPACK_SHORT_SPEC = 'SPACK_SHORT_SPEC'
SPACK_DEBUG_LOG_ID = 'SPACK_DEBUG_LOG_ID'
SPACK_DEBUG_LOG_DIR = 'SPACK_DEBUG_LOG_DIR'


# Platform-specific library suffix.
dso_suffix = 'dylib' if sys.platform == 'darwin' else 'so'


class MakeExecutable(Executable):
    """Special callable executable object for make so the user can
       specify parallel or not on a per-invocation basis.  Using
       'parallel' as a kwarg will override whatever the package's
       global setting is, so you can either default to true or false
       and override particular calls.

       Note that if the SPACK_NO_PARALLEL_MAKE env var is set it overrides
       everything.
    """

    def __init__(self, name, jobs):
        super(MakeExecutable, self).__init__(name)
        self.jobs = jobs

    def __call__(self, *args, **kwargs):
        disable = env_flag(SPACK_NO_PARALLEL_MAKE)
        parallel = not disable and kwargs.get('parallel', self.jobs > 1)

        if parallel:
            jobs = "-j%d" % self.jobs
            args = (jobs,) + args

        return super(MakeExecutable, self).__call__(*args, **kwargs)


def set_compiler_environment_variables(pkg, env):
    assert(pkg.spec.concrete)
    compiler = pkg.compiler

    # Set compiler variables used by CMake and autotools
    assert all(key in compiler.link_paths for key in (
        'cc', 'cxx', 'f77', 'fc'))

    # Populate an object with the list of environment modifications
    # and return it
    # TODO : add additional kwargs for better diagnostics, like requestor,
    # ttyout, ttyerr, etc.
    link_dir = spack.build_env_path

    # Set SPACK compiler variables so that our wrapper knows what to call
    if compiler.cc:
        env.set('SPACK_CC', compiler.cc)
        env.set('CC', join_path(link_dir, compiler.link_paths['cc']))
    if compiler.cxx:
        env.set('SPACK_CXX', compiler.cxx)
        env.set('CXX', join_path(link_dir, compiler.link_paths['cxx']))
    if compiler.f77:
        env.set('SPACK_F77', compiler.f77)
        env.set('F77', join_path(link_dir, compiler.link_paths['f77']))
    if compiler.fc:
        env.set('SPACK_FC',  compiler.fc)
        env.set('FC', join_path(link_dir, compiler.link_paths['fc']))

    # Set SPACK compiler rpath flags so that our wrapper knows what to use
    env.set('SPACK_CC_RPATH_ARG',  compiler.cc_rpath_arg)
    env.set('SPACK_CXX_RPATH_ARG', compiler.cxx_rpath_arg)
    env.set('SPACK_F77_RPATH_ARG', compiler.f77_rpath_arg)
    env.set('SPACK_FC_RPATH_ARG',  compiler.fc_rpath_arg)

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
        injf, envf, bsf = handler(pkg, flag, pkg.spec.compiler_flags[flag])
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

    env.set('SPACK_COMPILER_SPEC', str(pkg.spec.compiler))

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
    link_deps       = set(pkg.spec.traverse(
                          root=False, deptype=('link', 'include')))
    build_link_deps = build_deps | link_deps
    rpath_deps      = get_rpath_deps(pkg)

    build_run_prefixes  = [dep.prefix for dep in build_deps]
    link_prefixes       = [dep.prefix for dep in link_deps]
    build_link_prefixes = [dep.prefix for dep in build_link_deps]
    rpath_prefixes      = [dep.prefix for dep in rpath_deps]

    # add run-time dependencies of direct build-time dependencies:
    for build_dep in build_deps:
        for run_dep in build_dep.traverse(deptype='run'):
            build_run_prefixes.append(run_dep.prefix)

    # Filter out system paths: ['/', '/usr', '/usr/local']
    # These paths can be introduced into the build when an external package
    # is added as a dependency. The problem with these paths is that they often
    # contain hundreds of other packages installed in the same directory.
    # If these paths come first, they can overshadow Spack installations.
    build_run_prefixes  = filter_system_paths(build_run_prefixes)
    link_prefixes       = filter_system_paths(link_prefixes)
    build_link_prefixes = filter_system_paths(build_link_prefixes)
    rpath_prefixes      = filter_system_paths(rpath_prefixes)

    # Prefixes of all of the package's dependencies go in SPACK_DEPENDENCIES
    env.set_path(SPACK_DEPENDENCIES, build_link_prefixes)

    # These variables control compiler wrapper behavior
    env.set_path(SPACK_RPATH_DEPS, rpath_prefixes)
    env.set_path(SPACK_LINK_DEPS, link_prefixes)

    # Add dependencies to CMAKE_PREFIX_PATH
    env.set_path('CMAKE_PREFIX_PATH', build_link_prefixes)

    # Install prefix
    env.set(SPACK_PREFIX, pkg.prefix)

    # Install root prefix
    env.set(SPACK_INSTALL, spack.store.root)

    # Stuff in here sanitizes the build environment to eliminate
    # anything the user has set that may interfere.
    if not dirty:
        # Remove these vars from the environment during build because they
        # can affect how some packages find libraries.  We want to make
        # sure that builds never pull in unintended external dependencies.
        env.unset('LD_LIBRARY_PATH')
        env.unset('LIBRARY_PATH')
        env.unset('CPATH')
        env.unset('LD_RUN_PATH')
        env.unset('DYLD_LIBRARY_PATH')

        # Remove any macports installs from the PATH.  The macports ld can
        # cause conflicts with the built-in linker on el capitan.  Solves
        # assembler issues, e.g.:
        #    suffix or operands invalid for `movq'"
        path = get_path('PATH')
        for p in path:
            if '/macports/' in p:
                env.remove_path('PATH', p)

    # Set environment variables if specified for
    # the given compiler
    compiler = pkg.compiler
    environment = compiler.environment
    if 'set' in environment:
        env_to_set = environment['set']
        for key, value in iteritems(env_to_set):
            env.set('SPACK_ENV_SET_%s' % key, value)
            env.set('%s' % key, value)
        # Let shell know which variables to set
        env_variables = ":".join(env_to_set.keys())
        env.set('SPACK_ENV_TO_SET', env_variables)

    if compiler.extra_rpaths:
        extra_rpaths = ':'.join(compiler.extra_rpaths)
        env.set('SPACK_COMPILER_EXTRA_RPATHS', extra_rpaths)

    # Add bin directories from dependencies to the PATH for the build.
    for prefix in build_run_prefixes:
        for dirname in ['bin', 'bin64']:
            bin_dir = os.path.join(prefix, dirname)
            if os.path.isdir(bin_dir):
                env.prepend_path('PATH', bin_dir)

    # Add spack build environment path with compiler wrappers first in
    # the path. We add both spack.env_path, which includes default
    # wrappers (cc, c++, f77, f90), AND a subdirectory containing
    # compiler-specific symlinks.  The latter ensures that builds that
    # are sensitive to the *name* of the compiler see the right name
    # when we're building with the wrappers.
    #
    # Conflicts on case-insensitive systems (like "CC" and "cc") are
    # handled by putting one in the <build_env_path>/case-insensitive
    # directory.  Add that to the path too.
    env_paths = []
    compiler_specific = join_path(spack.build_env_path, pkg.compiler.name)
    for item in [spack.build_env_path, compiler_specific]:
        env_paths.append(item)
        ci = join_path(item, 'case-insensitive')
        if os.path.isdir(ci):
            env_paths.append(ci)

    for item in reversed(env_paths):
        env.prepend_path('PATH', item)
    env.set_path(SPACK_ENV_PATH, env_paths)

    # Working directory for the spack command itself, for debug logs.
    if spack.debug:
        env.set(SPACK_DEBUG, 'TRUE')
    env.set(SPACK_SHORT_SPEC, pkg.spec.short_spec)
    env.set(SPACK_DEBUG_LOG_ID, pkg.spec.format('${PACKAGE}-${HASH:7}'))
    env.set(SPACK_DEBUG_LOG_DIR, spack.spack_working_dir)

    # Add any pkgconfig directories to PKG_CONFIG_PATH
    for prefix in build_link_prefixes:
        for directory in ('lib', 'lib64', 'share'):
            pcdir = join_path(prefix, directory, 'pkgconfig')
            if os.path.isdir(pcdir):
                env.prepend_path('PKG_CONFIG_PATH', pcdir)

    return env


def set_module_variables_for_package(pkg, module):
    """Populate the module scope of install() with some useful functions.
       This makes things easier for package writers.
    """
    # number of jobs spack will build with.
    jobs = spack.build_jobs
    if not pkg.parallel:
        jobs = 1
    elif pkg.make_jobs:
        jobs = pkg.make_jobs

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

    m.cmake = Executable('cmake')
    m.ctest = Executable('ctest')

    # Standard CMake arguments
    m.std_cmake_args = spack.CMakePackage._std_args(pkg)

    # Put spack compiler paths in module scope.
    link_dir = spack.build_env_path
    m.spack_cc = join_path(link_dir, pkg.compiler.link_paths['cc'])
    m.spack_cxx = join_path(link_dir, pkg.compiler.link_paths['cxx'])
    m.spack_f77 = join_path(link_dir, pkg.compiler.link_paths['f77'])
    m.spack_fc = join_path(link_dir, pkg.compiler.link_paths['fc'])

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
    if 'linux' in arch:
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
            '-install_name {0}'.format(install_name),
            '-Wl,-force_load,{0}'.format(static_lib)
        ]

        if compat_version:
            compiler_args.append('-compatibility_version {0}'.format(
                compat_version))

        if version:
            compiler_args.append('-current_version {0}'.format(version))

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
        rpaths.append(get_path_from_module(pkg.compiler.modules[1]))
    return rpaths


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
    return spack.CMakePackage._std_args(pkg)


def parent_class_modules(cls):
    """
    Get list of super class modules that are all descend from spack.Package
    """
    if (not issubclass(cls, spack.package.Package) or
        issubclass(spack.package.Package, cls)):
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
        if dep.external_module:
            load_module(dep.external_module)


def setup_package(pkg, dirty):
    """Execute all environment setup routines."""
    spack_env = EnvironmentModifications()
    run_env = EnvironmentModifications()

    set_compiler_environment_variables(pkg, spack_env)
    set_build_environment_variables(pkg, spack_env, dirty)
    pkg.architecture.platform.setup_platform_environment(pkg, spack_env)

    # traverse in postorder so package can use vars from its dependencies
    spec = pkg.spec
    for dspec in pkg.spec.traverse(order='post', root=False,
                                   deptype=('build', 'test')):
        # If a user makes their own package repo, e.g.
        # spack.repos.mystuff.libelf.Libelf, and they inherit from
        # an existing class like spack.repos.original.libelf.Libelf,
        # then set the module variables for both classes so the
        # parent class can still use them if it gets called.
        spkg = dspec.package
        modules = parent_class_modules(spkg.__class__)
        for mod in modules:
            set_module_variables_for_package(spkg, mod)
        set_module_variables_for_package(spkg, spkg.module)

        # Allow dependencies to modify the module
        dpkg = dspec.package
        dpkg.setup_dependent_package(pkg.module, spec)
        dpkg.setup_dependent_environment(spack_env, run_env, spec)

    set_module_variables_for_package(pkg, pkg.module)
    pkg.setup_environment(spack_env, run_env)

    # Make sure nothing's strange about the Spack environment.
    validate(spack_env, tty.warn)
    spack_env.apply_modifications()

    # All module loads that otherwise would belong in previous functions
    # have to occur after the spack_env object has its modifications applied.
    # Otherwise the environment modifications could undo module changes, such
    # as unsetting LD_LIBRARY_PATH after a module changes it.
    for mod in pkg.compiler.modules:
        # Fixes issue https://github.com/spack/spack/issues/3153
        if os.environ.get("CRAY_CPU_TARGET") == "mic-knl":
            load_module("cce")
        load_module(mod)

    if pkg.architecture.target.module_name:
        load_module(pkg.architecture.target.module_name)

    load_external_modules(pkg)


def fork(pkg, function, dirty, fake):
    """Fork a child process to do part of a spack build.

    Args:

        pkg (PackageBase): package whose environment we should set up the
            forked process for.
        function (callable): argless function to run in the child
            process.
        dirty (bool): If True, do NOT clean the environment before
            building.
        fake (bool): If True, skip package setup b/c it's not a real build

    Usage::

        def child_fun():
            # do stuff
        build_env.fork(pkg, child_fun)

    Forked processes are run with the build environment set up by
    spack.build_environment.  This allows package authors to have full
    control over the environment, etc. without affecting other builds
    that might be executed in the same spack call.

    If something goes wrong, the child process catches the error and
    passes it to the parent wrapped in a ChildError.  The parent is
    expected to handle (or re-raise) the ChildError.
    """

    def child_process(child_pipe, input_stream):
        # We are in the child process. Python sets sys.stdin to
        # open(os.devnull) to prevent our process and its parent from
        # simultaneously reading from the original stdin. But, we assume
        # that the parent process is not going to read from it till we
        # are done with the child, so we undo Python's precaution.
        if input_stream is not None:
            sys.stdin = input_stream

        try:
            if not fake:
                setup_package(pkg, dirty=dirty)
            return_value = function()
            child_pipe.send(return_value)
        except StopIteration as e:
            # StopIteration is used to stop installations
            # before the final stage, mainly for debug purposes
            tty.msg(e)
            child_pipe.send(None)

        except BaseException:
            # catch ANYTHING that goes wrong in the child process
            exc_type, exc, tb = sys.exc_info()

            # Need to unwind the traceback in the child because traceback
            # objects can't be sent to the parent.
            tb_string = traceback.format_exc()

            # build up some context from the offending package so we can
            # show that, too.
            package_context = get_package_context(tb)

            build_log = None
            if hasattr(pkg, 'log_path'):
                build_log = pkg.log_path

            # make a pickleable exception to send to parent.
            msg = "%s: %s" % (exc_type.__name__, str(exc))

            ce = ChildError(msg,
                            exc_type.__module__,
                            exc_type.__name__,
                            tb_string, build_log, package_context)
            child_pipe.send(ce)

        finally:
            child_pipe.close()

    parent_pipe, child_pipe = multiprocessing.Pipe()
    input_stream = None
    try:
        # Forward sys.stdin when appropriate, to allow toggling verbosity
        if sys.stdin.isatty() and hasattr(sys.stdin, 'fileno'):
            input_stream = os.fdopen(os.dup(sys.stdin.fileno()))

        p = multiprocessing.Process(
            target=child_process, args=(child_pipe, input_stream))
        p.start()

    except InstallError as e:
        e.pkg = pkg
        raise

    finally:
        # Close the input stream in the parent process
        if input_stream is not None:
            input_stream.close()

    child_result = parent_pipe.recv()
    p.join()

    # let the caller know which package went wrong.
    if isinstance(child_result, InstallError):
        child_result.pkg = pkg

    # If the child process raised an error, print its output here rather
    # than waiting until the call to SpackError.die() in main(). This
    # allows exception handling output to be logged from within Spack.
    # see spack.main.SpackCommand.
    if isinstance(child_result, ChildError):
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

    # we found obj, the Package implementation we care about.
    # point out the location in the install method where we failed.
    lines = []
    lines.append("%s:%d, in %s:" % (
        inspect.getfile(frame.f_code), frame.f_lineno, frame.f_code.co_name
    ))

    # Build a message showing context in the install method.
    sourcelines, start = inspect.getsourcelines(frame)

    fl = frame.f_lineno - start
    start_ctx = max(0, fl - context)
    sourcelines = sourcelines[start_ctx:fl + context + 1]
    for i, line in enumerate(sourcelines):
        is_error = start_ctx + i == fl
        mark = ">> " if is_error else "   "
        marked = "  %s%-6d%s" % (mark, start_ctx + i, line.rstrip())
        if is_error:
            marked = colorize('@R{%s}' % marked)
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

    def __init__(self, msg, module, classname, traceback_string, build_log,
                 context):
        super(ChildError, self).__init__(msg)
        self.module = module
        self.name = classname
        self.traceback = traceback_string
        self.build_log = build_log
        self.context = context

    @property
    def long_message(self):
        out = StringIO()
        out.write(self._long_message if self._long_message else '')

        if (self.module, self.name) in ChildError.build_errors:
            # The error happened in some external executed process. Show
            # the build log with errors highlighted.
            if self.build_log:
                errors, warnings = parse_log_events(self.build_log)
                nerr = len(errors)
                if nerr > 0:
                    if nerr == 1:
                        out.write("\n1 error found in build log:\n")
                    else:
                        out.write("\n%d errors found in build log:\n" % nerr)
                    out.write(make_log_context(errors))

        else:
            # The error happened in in the Python code, so try to show
            # some context from the Package itself.
            out.write('%s: %s\n\n' % (self.name, self.message))
            if self.context:
                out.write('\n'.join(self.context))
                out.write('\n')

        if out.getvalue():
            out.write('\n')

        if self.build_log:
            out.write('See build log for details:\n')
            out.write('  %s' % self.build_log)

        return out.getvalue()

    def __str__(self):
        return self.message + self.long_message + self.traceback

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
            self.build_log,
            self.context)


def _make_child_error(msg, module, name, traceback, build_log, context):
    """Used by __reduce__ in ChildError to reconstruct pickled errors."""
    return ChildError(msg, module, name, traceback, build_log, context)
