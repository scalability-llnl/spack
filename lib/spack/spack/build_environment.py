# Copyright Spack Project Developers. See COPYRIGHT file for details.
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
import io
import multiprocessing
import os
import re
import stat
import sys
import traceback
import types
from collections import defaultdict
from enum import Flag, auto
from itertools import chain
from multiprocessing.connection import Connection
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    TextIO,
    Tuple,
    Type,
    Union,
    overload,
)

import archspec.cpu

import llnl.util.tty as tty
from llnl.string import plural
from llnl.util.filesystem import join_path
from llnl.util.lang import dedupe, stable_partition
from llnl.util.symlink import symlink
from llnl.util.tty.color import cescape, colorize

import spack.build_systems.cmake
import spack.build_systems.meson
import spack.build_systems.python
import spack.builder
import spack.compilers
import spack.config
import spack.deptypes as dt
import spack.error
import spack.multimethod
import spack.package_base
import spack.paths
import spack.platforms
import spack.schema.environment
import spack.spec
import spack.stage
import spack.store
import spack.subprocess_context
import spack.util.executable
import spack.util.libc
from spack import traverse
from spack.context import Context
from spack.error import InstallError, NoHeadersError, NoLibrariesError
from spack.install_test import spack_install_test_log
from spack.util.environment import (
    SYSTEM_DIR_CASE_ENTRY,
    EnvironmentModifications,
    env_flag,
    filter_system_paths,
    get_path,
    is_system_path,
    validate,
)
from spack.util.executable import Executable
from spack.util.log_parse import make_log_context, parse_log_events
from spack.util.module_cmd import load_module

#
# This can be set by the user to globally disable parallel builds.
#
SPACK_NO_PARALLEL_MAKE = "SPACK_NO_PARALLEL_MAKE"

#
# These environment variables are set by
# set_wrapper_variables and used to pass parameters to
# Spack's compiler wrappers.
#
SPACK_ENV_PATH = "SPACK_ENV_PATH"
SPACK_MANAGED_DIRS = "SPACK_MANAGED_DIRS"
SPACK_INCLUDE_DIRS = "SPACK_INCLUDE_DIRS"
SPACK_LINK_DIRS = "SPACK_LINK_DIRS"
SPACK_RPATH_DIRS = "SPACK_RPATH_DIRS"
SPACK_STORE_INCLUDE_DIRS = "SPACK_STORE_INCLUDE_DIRS"
SPACK_STORE_LINK_DIRS = "SPACK_STORE_LINK_DIRS"
SPACK_STORE_RPATH_DIRS = "SPACK_STORE_RPATH_DIRS"
SPACK_RPATH_DEPS = "SPACK_RPATH_DEPS"
SPACK_LINK_DEPS = "SPACK_LINK_DEPS"
SPACK_PREFIX = "SPACK_PREFIX"
SPACK_INSTALL = "SPACK_INSTALL"
SPACK_DEBUG = "SPACK_DEBUG"
SPACK_SHORT_SPEC = "SPACK_SHORT_SPEC"
SPACK_DEBUG_LOG_ID = "SPACK_DEBUG_LOG_ID"
SPACK_DEBUG_LOG_DIR = "SPACK_DEBUG_LOG_DIR"
SPACK_CCACHE_BINARY = "SPACK_CCACHE_BINARY"
SPACK_SYSTEM_DIRS = "SPACK_SYSTEM_DIRS"

# Platform-specific library suffix.
if sys.platform == "darwin":
    dso_suffix = "dylib"
elif sys.platform == "win32":
    dso_suffix = "dll"
else:
    dso_suffix = "so"

stat_suffix = "lib" if sys.platform == "win32" else "a"


def jobserver_enabled():
    """Returns true if a posix jobserver (make) is detected."""
    return "MAKEFLAGS" in os.environ and "--jobserver" in os.environ["MAKEFLAGS"]


def get_effective_jobs(jobs, parallel=True, supports_jobserver=False):
    """Return the number of jobs, or None if supports_jobserver and a jobserver is detected."""
    if not parallel or jobs <= 1 or env_flag(SPACK_NO_PARALLEL_MAKE):
        return 1
    if supports_jobserver and jobserver_enabled():
        return None
    return jobs


class MakeExecutable(Executable):
    """Special callable executable object for make so the user can specify parallelism options
    on a per-invocation basis.
    """

    def __init__(self, name: str, *, jobs: int, supports_jobserver: bool = True) -> None:
        super().__init__(name)
        self.supports_jobserver = supports_jobserver
        self.jobs = jobs

    @overload
    def __call__(
        self,
        *args: str,
        parallel: bool = ...,
        jobs_env: Optional[str] = ...,
        jobs_env_supports_jobserver: bool = ...,
        fail_on_error: bool = ...,
        ignore_errors: Union[int, Sequence[int]] = ...,
        ignore_quotes: Optional[bool] = ...,
        timeout: Optional[int] = ...,
        env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        extra_env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        input: Optional[TextIO] = ...,
        output: Union[Optional[TextIO], str] = ...,
        error: Union[Optional[TextIO], str] = ...,
        _dump_env: Optional[Dict[str, str]] = ...,
    ) -> None: ...

    @overload
    def __call__(
        self,
        *args: str,
        parallel: bool = ...,
        jobs_env: Optional[str] = ...,
        jobs_env_supports_jobserver: bool = ...,
        fail_on_error: bool = ...,
        ignore_errors: Union[int, Sequence[int]] = ...,
        ignore_quotes: Optional[bool] = ...,
        timeout: Optional[int] = ...,
        env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        extra_env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        input: Optional[TextIO] = ...,
        output: Union[Type[str], Callable] = ...,
        error: Union[Optional[TextIO], str, Type[str], Callable] = ...,
        _dump_env: Optional[Dict[str, str]] = ...,
    ) -> str: ...

    @overload
    def __call__(
        self,
        *args: str,
        parallel: bool = ...,
        jobs_env: Optional[str] = ...,
        jobs_env_supports_jobserver: bool = ...,
        fail_on_error: bool = ...,
        ignore_errors: Union[int, Sequence[int]] = ...,
        ignore_quotes: Optional[bool] = ...,
        timeout: Optional[int] = ...,
        env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        extra_env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        input: Optional[TextIO] = ...,
        output: Union[Optional[TextIO], str, Type[str], Callable] = ...,
        error: Union[Type[str], Callable] = ...,
        _dump_env: Optional[Dict[str, str]] = ...,
    ) -> str: ...

    def __call__(
        self,
        *args: str,
        parallel: bool = True,
        jobs_env: Optional[str] = None,
        jobs_env_supports_jobserver: bool = False,
        **kwargs,
    ) -> Optional[str]:
        """Runs this "make" executable in a subprocess.

        Args:
            parallel: if False, parallelism is disabled
            jobs_env: environment variable that will be set to the current level of parallelism
            jobs_env_supports_jobserver: whether the jobs env supports a job server

        For all the other **kwargs, refer to the base class.
        """
        jobs = get_effective_jobs(
            self.jobs, parallel=parallel, supports_jobserver=self.supports_jobserver
        )
        if jobs is not None:
            args = (f"-j{jobs}",) + args

        if jobs_env:
            # Caller wants us to set an environment variable to control the parallelism
            jobs_env_jobs = get_effective_jobs(
                self.jobs, parallel=parallel, supports_jobserver=jobs_env_supports_jobserver
            )
            if jobs_env_jobs is not None:
                extra_env = kwargs.setdefault("extra_env", {})
                extra_env.update({jobs_env: str(jobs_env_jobs)})

        return super().__call__(*args, **kwargs)


class UndeclaredDependencyError(spack.error.SpackError):
    """Raised if a dependency is invoking an executable through a module global, without
    declaring a dependency on it.
    """


class DeprecatedExecutable:
    def __init__(self, pkg: str, exe: str, exe_pkg: str) -> None:
        self.pkg = pkg
        self.exe = exe
        self.exe_pkg = exe_pkg

    def __call__(self, *args, **kwargs):
        raise UndeclaredDependencyError(
            f"{self.pkg} is using {self.exe} without declaring a dependency on {self.exe_pkg}"
        )

    def add_default_env(self, key: str, value: str):
        self.__call__()


def clean_environment():
    # Stuff in here sanitizes the build environment to eliminate
    # anything the user has set that may interfere. We apply it immediately
    # unlike the other functions so it doesn't overwrite what the modules load.
    env = EnvironmentModifications()

    # Remove these vars from the environment during build because they
    # can affect how some packages find libraries.  We want to make
    # sure that builds never pull in unintended external dependencies.
    env.unset("LD_LIBRARY_PATH")
    env.unset("LD_RUN_PATH")
    env.unset("DYLD_LIBRARY_PATH")
    env.unset("DYLD_FALLBACK_LIBRARY_PATH")

    # These vars affect how the compiler finds libraries and include dirs.
    env.unset("LIBRARY_PATH")
    env.unset("CPATH")
    env.unset("C_INCLUDE_PATH")
    env.unset("CPLUS_INCLUDE_PATH")
    env.unset("OBJC_INCLUDE_PATH")

    env.unset("CMAKE_PREFIX_PATH")
    env.unset("PYTHONPATH")
    env.unset("R_HOME")
    env.unset("R_ENVIRON")

    env.unset("LUA_PATH")
    env.unset("LUA_CPATH")

    # Affects GNU make, can e.g. indirectly inhibit enabling parallel build
    # env.unset('MAKEFLAGS')

    # Avoid that libraries of build dependencies get hijacked.
    env.unset("LD_PRELOAD")
    env.unset("DYLD_INSERT_LIBRARIES")

    # Avoid <packagename>_ROOT user variables overriding spack dependencies
    # https://cmake.org/cmake/help/latest/variable/PackageName_ROOT.html
    # Spack needs SPACK_ROOT though, so we need to exclude that
    for varname in os.environ.keys():
        if varname.endswith("_ROOT") and varname != "SPACK_ROOT":
            env.unset(varname)

    # Unset the following variables because they can affect installation of
    # Autotools and CMake packages.
    build_system_vars = [
        "CC",
        "CFLAGS",
        "CPP",
        "CPPFLAGS",  # C variables
        "CXX",
        "CCC",
        "CXXFLAGS",
        "CXXCPP",  # C++ variables
        "F77",
        "FFLAGS",
        "FLIBS",  # Fortran77 variables
        "FC",
        "FCFLAGS",
        "FCLIBS",  # Fortran variables
        "LDFLAGS",
        "LIBS",  # linker variables
    ]
    for v in build_system_vars:
        env.unset(v)

    # Unset mpi environment vars. These flags should only be set by
    # mpi providers for packages with mpi dependencies
    mpi_vars = ["MPICC", "MPICXX", "MPIFC", "MPIF77", "MPIF90"]
    for v in mpi_vars:
        env.unset(v)

    build_lang = spack.config.get("config:build_language")
    if build_lang:
        # Override language-related variables. This can be used to force
        # English compiler messages etc., which allows parse_log_events to
        # show useful matches.
        env.set("LC_ALL", build_lang)

    # Remove any macports installs from the PATH.  The macports ld can
    # cause conflicts with the built-in linker on el capitan.  Solves
    # assembler issues, e.g.:
    #    suffix or operands invalid for `movq'"
    path = get_path("PATH")
    for p in path:
        if "/macports/" in p:
            env.remove_path("PATH", p)

    return env


def _add_werror_handling(keep_werror, env):
    keep_flags = set()
    # set of pairs
    replace_flags: List[Tuple[str, str]] = []
    if keep_werror == "all":
        keep_flags.add("-Werror*")
    else:
        if keep_werror == "specific":
            keep_flags.add("-Werror-*")
            keep_flags.add("-Werror=*")
        # This extra case is to handle -Werror-implicit-function-declaration
        replace_flags.append(("-Werror-", "-Wno-error="))
        replace_flags.append(("-Werror", "-Wno-error"))
    env.set("SPACK_COMPILER_FLAGS_KEEP", "|".join(keep_flags))
    env.set("SPACK_COMPILER_FLAGS_REPLACE", " ".join(["|".join(item) for item in replace_flags]))


def set_compiler_environment_variables(pkg, env):
    assert pkg.spec.concrete
    compiler = pkg.compiler
    spec = pkg.spec

    # Make sure the executables for this compiler exist
    compiler.verify_executables()

    # Set compiler variables used by CMake and autotools
    assert all(key in compiler.link_paths for key in ("cc", "cxx", "f77", "fc"))

    # Populate an object with the list of environment modifications
    # and return it
    # TODO : add additional kwargs for better diagnostics, like requestor,
    # ttyout, ttyerr, etc.
    link_dir = spack.paths.build_env_path

    # Set SPACK compiler variables so that our wrapper knows what to
    # call.  If there is no compiler configured then use a default
    # wrapper which will emit an error if it is used.
    if compiler.cc:
        env.set("SPACK_CC", compiler.cc)
        env.set("CC", os.path.join(link_dir, compiler.link_paths["cc"]))
    else:
        env.set("CC", os.path.join(link_dir, "cc"))
    if compiler.cxx:
        env.set("SPACK_CXX", compiler.cxx)
        env.set("CXX", os.path.join(link_dir, compiler.link_paths["cxx"]))
    else:
        env.set("CC", os.path.join(link_dir, "c++"))
    if compiler.f77:
        env.set("SPACK_F77", compiler.f77)
        env.set("F77", os.path.join(link_dir, compiler.link_paths["f77"]))
    else:
        env.set("F77", os.path.join(link_dir, "f77"))
    if compiler.fc:
        env.set("SPACK_FC", compiler.fc)
        env.set("FC", os.path.join(link_dir, compiler.link_paths["fc"]))
    else:
        env.set("FC", os.path.join(link_dir, "fc"))

    # Set SPACK compiler rpath flags so that our wrapper knows what to use
    env.set("SPACK_CC_RPATH_ARG", compiler.cc_rpath_arg)
    env.set("SPACK_CXX_RPATH_ARG", compiler.cxx_rpath_arg)
    env.set("SPACK_F77_RPATH_ARG", compiler.f77_rpath_arg)
    env.set("SPACK_FC_RPATH_ARG", compiler.fc_rpath_arg)
    env.set("SPACK_LINKER_ARG", compiler.linker_arg)

    # Check whether we want to force RPATH or RUNPATH
    if spack.config.get("config:shared_linking:type") == "rpath":
        env.set("SPACK_DTAGS_TO_STRIP", compiler.enable_new_dtags)
        env.set("SPACK_DTAGS_TO_ADD", compiler.disable_new_dtags)
    else:
        env.set("SPACK_DTAGS_TO_STRIP", compiler.disable_new_dtags)
        env.set("SPACK_DTAGS_TO_ADD", compiler.enable_new_dtags)

    if pkg.keep_werror is not None:
        keep_werror = pkg.keep_werror
    else:
        keep_werror = spack.config.get("config:flags:keep_werror")

    _add_werror_handling(keep_werror, env)

    # Set the target parameters that the compiler will add
    isa_arg = optimization_flags(compiler, spec.target)
    env.set("SPACK_TARGET_ARGS", isa_arg)

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
            handler = pkg.flag_handler.__func__

        injf, envf, bsf = handler(pkg, flag, spec.compiler_flags[flag][:])
        inject_flags[flag] = injf or []
        env_flags[flag] = envf or []
        build_system_flags[flag] = bsf or []

    # Place compiler flags as specified by flag_handler
    for flag in spack.spec.FlagMap.valid_compiler_flags():
        # Concreteness guarantees key safety here
        if inject_flags[flag]:
            # variables SPACK_<FLAG> inject flags through wrapper
            var_name = "SPACK_{0}".format(flag.upper())
            env.set(var_name, " ".join(f for f in inject_flags[flag]))
        if env_flags[flag]:
            # implicit variables
            env.set(flag.upper(), " ".join(f for f in env_flags[flag]))
    pkg.flags_to_build_system_args(build_system_flags)

    env.set("SPACK_COMPILER_SPEC", str(spec.compiler))

    env.set("SPACK_SYSTEM_DIRS", SYSTEM_DIR_CASE_ENTRY)

    compiler.setup_custom_environment(pkg, env)

    return env


def optimization_flags(compiler, target):
    if spack.compilers.is_mixed_toolchain(compiler):
        msg = (
            "microarchitecture specific optimizations are not "
            "supported yet on mixed compiler toolchains [check"
            f" {compiler.name}@{compiler.version} for further details]"
        )
        tty.debug(msg)
        return ""

    # Try to check if the current compiler comes with a version number or
    # has an unexpected suffix. If so, treat it as a compiler with a
    # custom spec.
    compiler_version = compiler.version
    version_number, suffix = archspec.cpu.version_components(compiler.version)
    if not version_number or suffix:
        try:
            compiler_version = compiler.real_version
        except spack.util.executable.ProcessError as e:
            # log this and just return compiler.version instead
            tty.debug(str(e))

    try:
        result = target.optimization_flags(compiler.name, compiler_version.dotted_numeric_string)
    except (ValueError, archspec.cpu.UnsupportedMicroarchitecture):
        result = ""

    return result


class FilterDefaultDynamicLinkerSearchPaths:
    """Remove rpaths to directories that are default search paths of the dynamic linker."""

    def __init__(self, dynamic_linker: Optional[str]) -> None:
        # Identify directories by (inode, device) tuple, which handles symlinks too.
        self.default_path_identifiers: Set[Tuple[int, int]] = set()
        if not dynamic_linker:
            return
        for path in spack.util.libc.default_search_paths_from_dynamic_linker(dynamic_linker):
            try:
                s = os.stat(path)
                if stat.S_ISDIR(s.st_mode):
                    self.default_path_identifiers.add((s.st_ino, s.st_dev))
            except OSError:
                continue

    def is_dynamic_loader_default_path(self, p: str) -> bool:
        try:
            s = os.stat(p)
            return (s.st_ino, s.st_dev) in self.default_path_identifiers
        except OSError:
            return False

    def __call__(self, dirs: List[str]) -> List[str]:
        if not self.default_path_identifiers:
            return dirs
        return [p for p in dirs if not self.is_dynamic_loader_default_path(p)]


def set_wrapper_variables(pkg, env):
    """Set environment variables used by the Spack compiler wrapper (which have the prefix
    `SPACK_`) and also add the compiler wrappers to PATH.

    This determines the injected -L/-I/-rpath options; each of these specifies a search order and
    this function computes these options in a manner that is intended to match the DAG traversal
    order in `SetupContext`. TODO: this is not the case yet, we're using post order, SetupContext
    is using topo order."""
    # Set environment variables if specified for
    # the given compiler
    compiler = pkg.compiler
    env.extend(spack.schema.environment.parse(compiler.environment))

    if compiler.extra_rpaths:
        extra_rpaths = ":".join(compiler.extra_rpaths)
        env.set("SPACK_COMPILER_EXTRA_RPATHS", extra_rpaths)

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
        spack.paths.build_env_path, os.path.dirname(pkg.compiler.link_paths["cc"])
    )
    for item in [spack.paths.build_env_path, compiler_specific]:
        env_paths.append(item)
        ci = os.path.join(item, "case-insensitive")
        if os.path.isdir(ci):
            env_paths.append(ci)

    tty.debug("Adding compiler bin/ paths: " + " ".join(env_paths))
    for item in env_paths:
        env.prepend_path("PATH", item)
    env.set_path(SPACK_ENV_PATH, env_paths)

    # Working directory for the spack command itself, for debug logs.
    if spack.config.get("config:debug"):
        env.set(SPACK_DEBUG, "TRUE")
    env.set(SPACK_SHORT_SPEC, pkg.spec.short_spec)
    env.set(SPACK_DEBUG_LOG_ID, pkg.spec.format("{name}-{hash:7}"))
    env.set(SPACK_DEBUG_LOG_DIR, spack.paths.spack_working_dir)

    if spack.config.get("config:ccache"):
        # Enable ccache in the compiler wrapper
        env.set(SPACK_CCACHE_BINARY, spack.util.executable.which_string("ccache", required=True))
    else:
        # Avoid cache pollution if a build system forces `ccache <compiler wrapper invocation>`.
        env.set("CCACHE_DISABLE", "1")

    # Gather information about various types of dependencies
    rpath_hashes = set(s.dag_hash() for s in get_rpath_deps(pkg))
    link_deps = pkg.spec.traverse(root=False, order="topo", deptype=dt.LINK)
    external_link_deps, nonexternal_link_deps = stable_partition(link_deps, lambda d: d.external)

    link_dirs = []
    include_dirs = []
    rpath_dirs = []

    for dep in chain(external_link_deps, nonexternal_link_deps):
        # TODO: is_system_path is wrong, but even if we knew default -L, -I flags from the compiler
        # and default search dirs from the dynamic linker, it's not obvious how to avoid a possibly
        # expensive search in `query.libs.directories` and `query.headers.directories`, which is
        # what this branch is trying to avoid.
        if is_system_path(dep.prefix):
            continue
        # TODO: as of Spack 0.22, multiple instances of the same package may occur among the link
        # deps, so keying by name is wrong. In practice it is not problematic: we obtain the same
        # gcc-runtime / glibc here, and repeatedly add the same dirs that are later deduped.
        query = pkg.spec[dep.name]
        dep_link_dirs = []
        try:
            # Locating libraries can be time consuming, so log start and finish.
            tty.debug(f"Collecting libraries for {dep.name}")
            dep_link_dirs.extend(query.libs.directories)
            tty.debug(f"Libraries for {dep.name} have been collected.")
        except NoLibrariesError:
            tty.debug(f"No libraries found for {dep.name}")

        for default_lib_dir in ("lib", "lib64"):
            default_lib_prefix = os.path.join(dep.prefix, default_lib_dir)
            if os.path.isdir(default_lib_prefix):
                dep_link_dirs.append(default_lib_prefix)

        link_dirs[:0] = dep_link_dirs
        if dep.dag_hash() in rpath_hashes:
            rpath_dirs[:0] = dep_link_dirs

        try:
            tty.debug(f"Collecting headers for {dep.name}")
            include_dirs[:0] = query.headers.directories
            tty.debug(f"Headers for {dep.name} have been collected.")
        except NoHeadersError:
            tty.debug(f"No headers found for {dep.name}")

    # The top-level package is heuristically rpath'ed.
    for libdir in ("lib64", "lib"):
        lib_path = os.path.join(pkg.prefix, libdir)
        rpath_dirs.insert(0, lib_path)

    filter_default_dynamic_linker_search_paths = FilterDefaultDynamicLinkerSearchPaths(
        pkg.compiler.default_dynamic_linker
    )

    # TODO: filter_system_paths is again wrong (and probably unnecessary due to the is_system_path
    # branch above). link_dirs should be filtered with entries from _parse_link_paths.
    link_dirs = list(dedupe(filter_system_paths(link_dirs)))
    include_dirs = list(dedupe(filter_system_paths(include_dirs)))
    rpath_dirs = list(dedupe(filter_system_paths(rpath_dirs)))
    rpath_dirs = filter_default_dynamic_linker_search_paths(rpath_dirs)

    # TODO: implicit_rpaths is prefiltered by is_system_path, that should be removed in favor of
    # just this filter.
    implicit_rpaths = filter_default_dynamic_linker_search_paths(pkg.compiler.implicit_rpaths())
    if implicit_rpaths:
        env.set("SPACK_COMPILER_IMPLICIT_RPATHS", ":".join(implicit_rpaths))

    # Spack managed directories include the stage, store and upstream stores. We extend this with
    # their real paths to make it more robust (e.g. /tmp vs /private/tmp on macOS).
    spack_managed_dirs: Set[str] = {
        spack.stage.get_stage_root(),
        spack.store.STORE.db.root,
        *(db.root for db in spack.store.STORE.db.upstream_dbs),
    }
    spack_managed_dirs.update([os.path.realpath(p) for p in spack_managed_dirs])

    env.set(SPACK_MANAGED_DIRS, "|".join(f'"{p}/"*' for p in sorted(spack_managed_dirs)))
    is_spack_managed = lambda p: any(p.startswith(store) for store in spack_managed_dirs)
    link_dirs_spack, link_dirs_system = stable_partition(link_dirs, is_spack_managed)
    include_dirs_spack, include_dirs_system = stable_partition(include_dirs, is_spack_managed)
    rpath_dirs_spack, rpath_dirs_system = stable_partition(rpath_dirs, is_spack_managed)
    env.set(SPACK_LINK_DIRS, ":".join(link_dirs_system))
    env.set(SPACK_INCLUDE_DIRS, ":".join(include_dirs_system))
    env.set(SPACK_RPATH_DIRS, ":".join(rpath_dirs_system))
    env.set(SPACK_STORE_LINK_DIRS, ":".join(link_dirs_spack))
    env.set(SPACK_STORE_INCLUDE_DIRS, ":".join(include_dirs_spack))
    env.set(SPACK_STORE_RPATH_DIRS, ":".join(rpath_dirs_spack))


def set_package_py_globals(pkg, context: Context = Context.BUILD):
    """Populate the Python module of a package with some useful global names.
    This makes things easier for package writers.
    """
    module = ModuleChangePropagator(pkg)

    jobs = spack.config.determine_number_of_jobs(parallel=pkg.parallel)
    module.make_jobs = jobs
    if context == Context.BUILD:
        module.std_meson_args = spack.build_systems.meson.MesonBuilder.std_args(pkg)
        module.std_pip_args = spack.build_systems.python.PythonPipBuilder.std_args(pkg)

    module.make = DeprecatedExecutable(pkg.name, "make", "gmake")
    module.gmake = DeprecatedExecutable(pkg.name, "gmake", "gmake")
    module.ninja = DeprecatedExecutable(pkg.name, "ninja", "ninja")
    # TODO: johnwparent: add package or builder support to define these build tools
    # for now there is no entrypoint for builders to define these on their
    # own
    if sys.platform == "win32":
        module.nmake = Executable("nmake")
        module.msbuild = Executable("msbuild")
        # analog to configure for win32
        module.cscript = Executable("cscript")

    # Find the configure script in the archive path
    # Don't use which for this; we want to find it in the current dir.
    module.configure = Executable("./configure")

    # Put spack compiler paths in module scope. (Some packages use it
    # in setup_run_environment etc, so don't put it context == build)
    link_dir = spack.paths.build_env_path
    pkg_compiler = None
    try:
        pkg_compiler = pkg.compiler
    except spack.compilers.NoCompilerForSpecError as e:
        tty.debug(f"cannot set 'spack_cc': {str(e)}")

    if pkg_compiler is not None:
        module.spack_cc = os.path.join(link_dir, pkg_compiler.link_paths["cc"])
        module.spack_cxx = os.path.join(link_dir, pkg_compiler.link_paths["cxx"])
        module.spack_f77 = os.path.join(link_dir, pkg_compiler.link_paths["f77"])
        module.spack_fc = os.path.join(link_dir, pkg_compiler.link_paths["fc"])
    else:
        module.spack_cc = None
        module.spack_cxx = None
        module.spack_f77 = None
        module.spack_fc = None

    # Useful directories within the prefix are encapsulated in
    # a Prefix object.
    module.prefix = pkg.prefix

    # Platform-specific library suffix.
    module.dso_suffix = dso_suffix

    def static_to_shared_library(static_lib, shared_lib=None, **kwargs):
        compiler_path = kwargs.get("compiler", module.spack_cc)
        compiler = Executable(compiler_path)

        return _static_to_shared_library(
            pkg.spec.architecture, compiler, static_lib, shared_lib, **kwargs
        )

    module.static_to_shared_library = static_to_shared_library

    module.propagate_changes_to_mro()


def _static_to_shared_library(arch, compiler, static_lib, shared_lib=None, **kwargs):
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
    compiler_output = kwargs.get("compiler_output", None)
    arguments = kwargs.get("arguments", [])
    version = kwargs.get("version", None)
    compat_version = kwargs.get("compat_version", version)

    if not shared_lib:
        shared_lib = "{0}.{1}".format(os.path.splitext(static_lib)[0], dso_suffix)

    compiler_args = []

    # TODO: Compiler arguments should not be hardcoded but provided by
    #       the different compiler classes.
    if "linux" in arch or "cray" in arch:
        soname = os.path.basename(shared_lib)

        if compat_version:
            soname += ".{0}".format(compat_version)

        compiler_args = [
            "-shared",
            "-Wl,-soname,{0}".format(soname),
            "-Wl,--whole-archive",
            static_lib,
            "-Wl,--no-whole-archive",
        ]
    elif "darwin" in arch:
        install_name = shared_lib

        if compat_version:
            install_name += ".{0}".format(compat_version)

        compiler_args = [
            "-dynamiclib",
            "-install_name",
            "{0}".format(install_name),
            "-Wl,-force_load,{0}".format(static_lib),
        ]

        if compat_version:
            compiler_args.extend(["-compatibility_version", "{0}".format(compat_version)])

        if version:
            compiler_args.extend(["-current_version", "{0}".format(version)])

    if len(arguments) > 0:
        compiler_args.extend(arguments)

    shared_lib_base = shared_lib

    if version:
        shared_lib += ".{0}".format(version)
    elif compat_version:
        shared_lib += ".{0}".format(compat_version)

    compiler_args.extend(["-o", shared_lib])

    # Create symlinks for version and compat_version
    shared_lib_link = os.path.basename(shared_lib)

    if version or compat_version:
        symlink(shared_lib_link, shared_lib_base)

    if compat_version and compat_version != version:
        symlink(shared_lib_link, "{0}.{1}".format(shared_lib_base, compat_version))

    return compiler(*compiler_args, output=compiler_output)


def _get_rpath_deps_from_spec(
    spec: spack.spec.Spec, transitive_rpaths: bool
) -> List[spack.spec.Spec]:
    if not transitive_rpaths:
        return spec.dependencies(deptype=dt.LINK)

    by_name: Dict[str, spack.spec.Spec] = {}

    for dep in spec.traverse(root=False, deptype=dt.LINK):
        lookup = by_name.get(dep.name)
        if lookup is None:
            by_name[dep.name] = dep
        elif lookup.version < dep.version:
            by_name[dep.name] = dep

    return list(by_name.values())


def get_rpath_deps(pkg: spack.package_base.PackageBase) -> List[spack.spec.Spec]:
    """Return immediate or transitive dependencies (depending on the package) that need to be
    rpath'ed. If a package occurs multiple times, the newest version is kept."""
    return _get_rpath_deps_from_spec(pkg.spec, pkg.transitive_rpaths)


def load_external_modules(pkg):
    """Traverse a package's spec DAG and load any external modules.

    Traverse a package's dependencies and load any external modules
    associated with them.

    Args:
        pkg (spack.package_base.PackageBase): package to load deps for
    """
    for dep in list(pkg.spec.traverse()):
        external_modules = dep.external_modules or []
        for external_module in external_modules:
            load_module(external_module)


def setup_package(pkg, dirty, context: Context = Context.BUILD):
    """Execute all environment setup routines."""
    if context not in (Context.BUILD, Context.TEST):
        raise ValueError(f"'context' must be Context.BUILD or Context.TEST - got {context}")

    # First populate the package.py's module with the relevant globals that could be used in any
    # of the setup_* functions.
    setup_context = SetupContext(pkg.spec, context=context)
    setup_context.set_all_package_py_globals()

    # Keep track of env changes from packages separately, since we want to
    # issue warnings when packages make "suspicious" modifications.
    env_base = EnvironmentModifications() if dirty else clean_environment()
    env_mods = EnvironmentModifications()

    # setup compilers for build contexts
    need_compiler = context == Context.BUILD or (
        context == Context.TEST and pkg.test_requires_compiler
    )
    if need_compiler:
        set_compiler_environment_variables(pkg, env_mods)
        set_wrapper_variables(pkg, env_mods)

    # Platform specific setup goes before package specific setup. This is for setting
    # defaults like MACOSX_DEPLOYMENT_TARGET on macOS.
    platform = spack.platforms.by_name(pkg.spec.architecture.platform)
    platform.setup_platform_environment(pkg, env_mods)

    tty.debug("setup_package: grabbing modifications from dependencies")
    env_mods.extend(setup_context.get_env_modifications())
    tty.debug("setup_package: collected all modifications from dependencies")

    if context == Context.TEST:
        env_mods.prepend_path("PATH", ".")
    elif context == Context.BUILD and not dirty and not env_mods.is_unset("CPATH"):
        tty.debug(
            "A dependency has updated CPATH, this may lead pkg-config to assume that the package "
            "is part of the system includes and omit it when invoked with '--cflags'."
        )

    # First apply the clean environment changes
    env_base.apply_modifications()

    # Load modules on an already clean environment, just before applying Spack's
    # own environment modifications. This ensures Spack controls CC/CXX/... variables.
    if need_compiler:
        tty.debug("setup_package: loading compiler modules")
        for mod in pkg.compiler.modules:
            load_module(mod)

    load_external_modules(pkg)

    # Make sure nothing's strange about the Spack environment.
    validate(env_mods, tty.warn)
    env_mods.apply_modifications()

    # Return all env modifications we controlled (excluding module related ones)
    env_base.extend(env_mods)
    return env_base


class EnvironmentVisitor:
    def __init__(self, *roots: spack.spec.Spec, context: Context):
        # For the roots (well, marked specs) we follow different edges
        # than for their deps, depending on the context.
        self.root_hashes = set(s.dag_hash() for s in roots)

        if context == Context.BUILD:
            # Drop direct run deps in build context
            # We don't really distinguish between install and build time test deps,
            # so we include them here as build-time test deps.
            self.root_depflag = dt.BUILD | dt.TEST | dt.LINK
        elif context == Context.TEST:
            # This is more of an extended run environment
            self.root_depflag = dt.TEST | dt.RUN | dt.LINK
        elif context == Context.RUN:
            self.root_depflag = dt.RUN | dt.LINK

    def accept(self, item):
        return True

    def neighbors(self, item):
        spec = item.edge.spec
        if spec.dag_hash() in self.root_hashes:
            depflag = self.root_depflag
        else:
            depflag = dt.LINK | dt.RUN
        return traverse.sort_edges(spec.edges_to_dependencies(depflag=depflag))


class UseMode(Flag):
    #: Entrypoint spec (a spec to be built; an env root, etc)
    ROOT = auto()

    #: A spec used at runtime, but no executables in PATH
    RUNTIME = auto()

    #: A spec used at runtime, with executables in PATH
    RUNTIME_EXECUTABLE = auto()

    #: A spec that's a direct build or test dep
    BUILDTIME_DIRECT = auto()

    #: A spec that should be visible in search paths in a build env.
    BUILDTIME = auto()

    #: Flag is set when the (node, mode) is finalized
    ADDED = auto()


def effective_deptypes(
    *specs: spack.spec.Spec, context: Context = Context.BUILD
) -> List[Tuple[spack.spec.Spec, UseMode]]:
    """Given a list of input specs and a context, return a list of tuples of
    all specs that contribute to (environment) modifications, together with
    a flag specifying in what way they do so. The list is ordered topologically
    from root to leaf, meaning that environment modifications should be applied
    in reverse so that dependents override dependencies, not the other way around."""
    topo_sorted_edges = traverse.traverse_topo_edges_generator(
        traverse.with_artificial_edges(specs),
        visitor=traverse.CoverEdgesVisitor(
            EnvironmentVisitor(*specs, context=context), key=traverse.by_dag_hash
        ),
        key=traverse.by_dag_hash,
        root=True,
        all_edges=True,
    )

    # Dictionary with "no mode" as default value, so it's easy to write modes[x] |= flag.
    use_modes = defaultdict(lambda: UseMode(0))
    nodes_with_type = []

    for edge in topo_sorted_edges:
        parent, child, depflag = edge.parent, edge.spec, edge.depflag

        # Mark the starting point
        if parent is None:
            use_modes[child] = UseMode.ROOT
            continue

        parent_mode = use_modes[parent]

        # Nothing to propagate.
        if not parent_mode:
            continue

        # Dependending on the context, include particular deps from the root.
        if UseMode.ROOT & parent_mode:
            if context == Context.BUILD:
                if (dt.BUILD | dt.TEST) & depflag:
                    use_modes[child] |= UseMode.BUILDTIME_DIRECT
                if dt.LINK & depflag:
                    use_modes[child] |= UseMode.BUILDTIME

            elif context == Context.TEST:
                if (dt.RUN | dt.TEST) & depflag:
                    use_modes[child] |= UseMode.RUNTIME_EXECUTABLE
                elif dt.LINK & depflag:
                    use_modes[child] |= UseMode.RUNTIME

            elif context == Context.RUN:
                if dt.RUN & depflag:
                    use_modes[child] |= UseMode.RUNTIME_EXECUTABLE
                elif dt.LINK & depflag:
                    use_modes[child] |= UseMode.RUNTIME

        # Propagate RUNTIME and RUNTIME_EXECUTABLE through link and run deps.
        if (UseMode.RUNTIME | UseMode.RUNTIME_EXECUTABLE | UseMode.BUILDTIME_DIRECT) & parent_mode:
            if dt.LINK & depflag:
                use_modes[child] |= UseMode.RUNTIME
            if dt.RUN & depflag:
                use_modes[child] |= UseMode.RUNTIME_EXECUTABLE

        # Propagate BUILDTIME through link deps.
        if UseMode.BUILDTIME & parent_mode:
            if dt.LINK & depflag:
                use_modes[child] |= UseMode.BUILDTIME

        # Finalize the spec; the invariant is that all in-edges are processed
        # before out-edges, meaning that parent is done.
        if not (UseMode.ADDED & parent_mode):
            use_modes[parent] |= UseMode.ADDED
            nodes_with_type.append((parent, parent_mode))

    # Attach the leaf nodes, since we only added nodes with out-edges.
    for spec, parent_mode in use_modes.items():
        if parent_mode and not (UseMode.ADDED & parent_mode):
            nodes_with_type.append((spec, parent_mode))

    return nodes_with_type


class SetupContext:
    """This class encapsulates the logic to determine environment modifications, and is used as
    well to set globals in modules of package.py."""

    def __init__(self, *specs: spack.spec.Spec, context: Context) -> None:
        """Construct a ModificationsFromDag object.
        Args:
            specs: single root spec for build/test context, possibly more for run context
            context: build, run, or test"""
        if (context == Context.BUILD or context == Context.TEST) and not len(specs) == 1:
            raise ValueError("Cannot setup build environment for multiple specs")
        specs_with_type = effective_deptypes(*specs, context=context)

        self.specs = specs
        self.context = context
        self.external: List[Tuple[spack.spec.Spec, UseMode]]
        self.nonexternal: List[Tuple[spack.spec.Spec, UseMode]]
        # Reverse so we go from leaf to root
        self.nodes_in_subdag = set(id(s) for s, _ in specs_with_type)

        # Split into non-external and external, maintaining topo order per group.
        self.external, self.nonexternal = stable_partition(
            reversed(specs_with_type), lambda t: t[0].external
        )
        self.should_be_runnable = UseMode.BUILDTIME_DIRECT | UseMode.RUNTIME_EXECUTABLE
        self.should_setup_run_env = (
            UseMode.BUILDTIME_DIRECT | UseMode.RUNTIME | UseMode.RUNTIME_EXECUTABLE
        )
        self.should_setup_dependent_build_env = UseMode.BUILDTIME | UseMode.BUILDTIME_DIRECT
        self.should_setup_build_env = UseMode.ROOT if context == Context.BUILD else UseMode(0)

        if context == Context.RUN or context == Context.TEST:
            self.should_be_runnable |= UseMode.ROOT
            self.should_setup_run_env |= UseMode.ROOT

        # Everything that calls setup_run_environment and setup_dependent_* needs globals set.
        self.should_set_package_py_globals = (
            self.should_setup_dependent_build_env | self.should_setup_run_env | UseMode.ROOT
        )
        # In a build context, the root needs build-specific globals set.
        self.needs_build_context = UseMode.ROOT

    def set_all_package_py_globals(self):
        """Set the globals in modules of package.py files."""
        for dspec, flag in chain(self.external, self.nonexternal):
            pkg = dspec.package

            if self.should_set_package_py_globals & flag:
                if self.context == Context.BUILD and self.needs_build_context & flag:
                    set_package_py_globals(pkg, context=Context.BUILD)
                else:
                    # This includes runtime dependencies, also runtime deps of direct build deps.
                    set_package_py_globals(pkg, context=Context.RUN)

        # Looping over the set of packages a second time
        # ensures all globals are loaded into the module space prior to
        # any package setup. This guarantees package setup methods have
        # access to expected module level definitions such as "spack_cc"
        for dspec, flag in chain(self.external, self.nonexternal):
            pkg = dspec.package
            for spec in dspec.dependents():
                # Note: some specs have dependents that are unreachable from the root, so avoid
                # setting globals for those.
                if id(spec) not in self.nodes_in_subdag:
                    continue
                dependent_module = ModuleChangePropagator(spec.package)
                pkg.setup_dependent_package(dependent_module, spec)
                dependent_module.propagate_changes_to_mro()

        if self.context == Context.BUILD:
            pkg = self.specs[0].package
            module = ModuleChangePropagator(pkg)
            # std_cmake_args is not sufficiently static to be defined
            # in set_package_py_globals and is deprecated so its handled
            # here as a special case
            module.std_cmake_args = spack.build_systems.cmake.CMakeBuilder.std_args(pkg)
            module.propagate_changes_to_mro()

    def get_env_modifications(self) -> EnvironmentModifications:
        """Returns the environment variable modifications for the given input specs and context.
        Environment modifications include:
        - Updating PATH for packages that are required at runtime
        - Updating CMAKE_PREFIX_PATH and PKG_CONFIG_PATH so that their respective
        tools can find Spack-built dependencies (when context=build)
        - Running custom package environment modifications: setup_run_environment,
        setup_dependent_run_environment, setup_build_environment,
        setup_dependent_build_environment.

        The (partial) order imposed on the specs is externals first, then topological
        from leaf to root. That way externals cannot contribute search paths that would shadow
        Spack's prefixes, and dependents override variables set by dependencies."""
        env = EnvironmentModifications()
        for dspec, flag in chain(self.external, self.nonexternal):
            tty.debug(f"Adding env modifications for {dspec.name}")
            pkg = dspec.package

            if self.should_setup_dependent_build_env & flag:
                self._make_buildtime_detectable(dspec, env)

                for root in self.specs:  # there is only one root in build context
                    spack.builder.create(pkg).setup_dependent_build_environment(env, root)

            if self.should_setup_build_env & flag:
                spack.builder.create(pkg).setup_build_environment(env)

            if self.should_be_runnable & flag:
                self._make_runnable(dspec, env)

            if self.should_setup_run_env & flag:
                run_env_mods = EnvironmentModifications()
                for spec in dspec.dependents(deptype=dt.LINK | dt.RUN):
                    if id(spec) in self.nodes_in_subdag:
                        pkg.setup_dependent_run_environment(run_env_mods, spec)
                pkg.setup_run_environment(run_env_mods)

                external_env = (dspec.extra_attributes or {}).get("environment", {})
                if external_env:
                    run_env_mods.extend(spack.schema.environment.parse(external_env))

                if self.context == Context.BUILD:
                    # Don't let the runtime environment of comiler like dependencies leak into the
                    # build env
                    run_env_mods.drop("CC", "CXX", "F77", "FC")
                env.extend(run_env_mods)

        return env

    def _make_buildtime_detectable(self, dep: spack.spec.Spec, env: EnvironmentModifications):
        if is_system_path(dep.prefix):
            return

        env.prepend_path("CMAKE_PREFIX_PATH", dep.prefix)
        for d in ("lib", "lib64", "share"):
            pcdir = os.path.join(dep.prefix, d, "pkgconfig")
            if os.path.isdir(pcdir):
                env.prepend_path("PKG_CONFIG_PATH", pcdir)

    def _make_runnable(self, dep: spack.spec.Spec, env: EnvironmentModifications):
        if is_system_path(dep.prefix):
            return

        for d in ("bin", "bin64"):
            bin_dir = os.path.join(dep.prefix, d)
            if os.path.isdir(bin_dir):
                env.prepend_path("PATH", bin_dir)


def _setup_pkg_and_run(
    serialized_pkg: "spack.subprocess_context.PackageInstallContext",
    function: Callable,
    kwargs: Dict,
    write_pipe: Connection,
    input_pipe: Optional[Connection],
    jsfd1: Optional[Connection],
    jsfd2: Optional[Connection],
):
    """Main entry point in the child process for Spack builds.

    ``_setup_pkg_and_run`` is called by the child process created in
    ``start_build_process()``, and its main job is to run ``function()`` on behalf of
    some Spack installation (see :ref:`spack.installer.PackageInstaller._install_task`).

    The child process is passed a ``write_pipe``, on which it's expected to send one of
    the following:

    * ``StopPhase``: error raised by a build process indicating it's stopping at a
      particular build phase.

    * ``BaseException``: any exception raised by a child build process, which will be
      wrapped in ``ChildError`` (which adds a bunch of debug info and log context) and
      raised in the parent.

    * The return value of ``function()``, which can be anything (except an exception).
      This is returned to the caller.

    Note: ``jsfd1`` and ``jsfd2`` are passed solely to ensure that the child process
    does not close these file descriptors. Some ``multiprocessing`` backends will close
    them automatically in the child if they are not passed at process creation time.

    Arguments:
        serialized_pkg: Spack package install context object (serialized form of the
            package that we'll build in the child process).
        function: function to call in the child process; serialized_pkg is passed to
            this as the first argument.
        kwargs: additional keyword arguments to pass to ``function()``.
        write_pipe: multiprocessing ``Connection`` to the parent process, to which the
            child *must* send a result (or an error) back to parent on.
        input_multiprocess_fd: stdin from the parent (not passed currently on Windows)
        jsfd1: gmake Jobserver file descriptor 1.
        jsfd2: gmake Jobserver file descriptor 2.

    """

    context: str = kwargs.get("context", "build")

    try:
        # We are in the child process. Python sets sys.stdin to open(os.devnull) to prevent our
        # process and its parent from simultaneously reading from the original stdin. But, we
        # assume that the parent process is not going to read from it till we are done with the
        # child, so we undo Python's precaution. closefd=False since Connection has ownership.
        if input_pipe is not None:
            sys.stdin = os.fdopen(input_pipe.fileno(), closefd=False)

        pkg = serialized_pkg.restore()

        if not kwargs.get("fake", False):
            kwargs["unmodified_env"] = os.environ.copy()
            kwargs["env_modifications"] = setup_package(
                pkg, dirty=kwargs.get("dirty", False), context=Context.from_string(context)
            )
        return_value = function(pkg, kwargs)
        write_pipe.send(return_value)

    except spack.error.StopPhase as e:
        # Do not create a full ChildError from this, it's not an error
        # it's a control statement.
        write_pipe.send(e)
    except BaseException as e:
        # catch ANYTHING that goes wrong in the child process

        # Need to unwind the traceback in the child because traceback
        # objects can't be sent to the parent.
        exc_type = type(e)
        tb = e.__traceback__
        tb_string = "".join(traceback.format_exception(exc_type, e, tb))

        # build up some context from the offending package so we can
        # show that, too.
        package_context = get_package_context(tb)

        logfile = None
        if context == "build":
            try:
                if hasattr(pkg, "log_path"):
                    logfile = pkg.log_path
            except NameError:
                # 'pkg' is not defined yet
                pass
        elif context == "test":
            logfile = os.path.join(pkg.test_suite.stage, pkg.test_suite.test_log_name(pkg.spec))

        error_msg = str(e)
        if isinstance(e, (spack.multimethod.NoSuchMethodError, AttributeError)):
            process = "test the installation" if context == "test" else "build from sources"
            error_msg = (
                "The '{}' package cannot find an attribute while trying to {}. "
                "This might be due to a change in Spack's package format "
                "to support multiple build-systems for a single package. You can fix this "
                "by updating the {} recipe, and you can also report the issue as a bug. "
                "More information at https://spack.readthedocs.io/en/latest/packaging_guide.html#installation-procedure"
            ).format(pkg.name, process, context)
            error_msg = colorize("@*R{{{}}}".format(error_msg))
            error_msg = "{}\n\n{}".format(str(e), error_msg)

        # make a pickleable exception to send to parent.
        msg = "%s: %s" % (exc_type.__name__, error_msg)

        ce = ChildError(
            msg,
            exc_type.__module__,
            exc_type.__name__,
            tb_string,
            logfile,
            context,
            package_context,
        )
        write_pipe.send(ce)

    finally:
        write_pipe.close()
        if input_pipe is not None:
            input_pipe.close()


def start_build_process(pkg, function, kwargs):
    """Create a child process to do part of a spack build.

    Args:

        pkg (spack.package_base.PackageBase): package whose environment we should set up the
            child process for.
        function (typing.Callable): argless function to run in the child
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
    """
    read_pipe, write_pipe = multiprocessing.Pipe(duplex=False)
    input_fd = None
    jobserver_fd1 = None
    jobserver_fd2 = None

    serialized_pkg = spack.subprocess_context.PackageInstallContext(pkg)

    try:
        # Forward sys.stdin when appropriate, to allow toggling verbosity
        if sys.platform != "win32" and sys.stdin.isatty() and hasattr(sys.stdin, "fileno"):
            input_fd = Connection(os.dup(sys.stdin.fileno()))
        mflags = os.environ.get("MAKEFLAGS", False)
        if mflags:
            m = re.search(r"--jobserver-[^=]*=(\d),(\d)", mflags)
            if m:
                jobserver_fd1 = Connection(int(m.group(1)))
                jobserver_fd2 = Connection(int(m.group(2)))

        p = multiprocessing.Process(
            target=_setup_pkg_and_run,
            args=(
                serialized_pkg,
                function,
                kwargs,
                write_pipe,
                input_fd,
                jobserver_fd1,
                jobserver_fd2,
            ),
        )

        p.start()

        # We close the writable end of the pipe now to be sure that p is the
        # only process which owns a handle for it. This ensures that when p
        # closes its handle for the writable end, read_pipe.recv() will
        # promptly report the readable end as being ready.
        write_pipe.close()

    except InstallError as e:
        e.pkg = pkg
        raise

    finally:
        # Close the input stream in the parent process
        if input_fd is not None:
            input_fd.close()

    def exitcode_msg(p):
        typ = "exit" if p.exitcode >= 0 else "signal"
        return f"{typ} {abs(p.exitcode)}"

    try:
        child_result = read_pipe.recv()
    except EOFError:
        p.join()
        raise InstallError(f"The process has stopped unexpectedly ({exitcode_msg(p)})")

    p.join()

    # If returns a StopPhase, raise it
    if isinstance(child_result, spack.error.StopPhase):
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

    # Fallback. Usually caught beforehand in EOFError above.
    if p.exitcode != 0:
        raise InstallError(f"The process failed unexpectedly ({exitcode_msg(p)})")

    return child_result


CONTEXT_BASES = (spack.package_base.PackageBase, spack.builder.Builder)


def get_package_context(traceback, context=3):
    """Return some context for an error message when the build fails.

    Args:
        traceback: A traceback from some exception raised during
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

    basenames = tuple(base.__name__ for base in CONTEXT_BASES)
    for tb in stack:
        frame = tb.tb_frame
        if "self" in frame.f_locals:
            # Find the first proper subclass of the PackageBase or BaseBuilder, but
            # don't provide context if the code is actually in the base classes.
            obj = frame.f_locals["self"]
            func = getattr(obj, tb.tb_frame.f_code.co_name, "")
            if func and hasattr(func, "__qualname__"):
                typename, *_ = func.__qualname__.partition(".")
                if isinstance(obj, CONTEXT_BASES) and typename not in basenames:
                    break
    else:
        return None

    # We found obj, the Package implementation we care about.
    # Point out the location in the install method where we failed.
    filename = inspect.getfile(frame.f_code)
    lines = [f"{filename}:{frame.f_lineno}, in {frame.f_code.co_name}:"]

    # Build a message showing context in the install method.
    sourcelines, start = inspect.getsourcelines(frame)

    # Calculate lineno of the error relative to the start of the function.
    fun_lineno = frame.f_lineno - start
    start_ctx = max(0, fun_lineno - context)
    sourcelines = sourcelines[start_ctx : fun_lineno + context + 1]

    for i, line in enumerate(sourcelines):
        is_error = start_ctx + i == fun_lineno
        # Add start to get lineno relative to start of file, not function.
        marked = f"  {'>> ' if is_error else '   '}{start + start_ctx + i:-6d}{line.rstrip()}"
        if is_error:
            marked = colorize("@R{%s}" % cescape(marked))
        lines.append(marked)

    return lines


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
    build_errors = [("spack.util.executable", "ProcessError")]

    def __init__(self, msg, module, classname, traceback_string, log_name, log_type, context):
        super().__init__(msg)
        self.module = module
        self.name = classname
        self.traceback = traceback_string
        self.log_name = log_name
        self.log_type = log_type
        self.context = context

    @property
    def long_message(self):
        out = io.StringIO()
        out.write(self._long_message if self._long_message else "")

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
                out.write("\n")
                out.write("\n".join(self.context))
                out.write("\n")

        if out.getvalue():
            out.write("\n")

        if have_log:
            out.write("See {0} log for details:\n".format(self.log_type))
            out.write("  {0}\n".format(self.log_name))

        # Also output the test log path IF it exists
        if self.context != "test" and have_log:
            test_log = join_path(os.path.dirname(self.log_name), spack_install_test_log)
            if os.path.isfile(test_log):
                out.write("\nSee test log for details:\n")
                out.write("  {0}\n".format(test_log))

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
            self.context,
        )


def _make_child_error(msg, module, name, traceback, log, log_type, context):
    """Used by __reduce__ in ChildError to reconstruct pickled errors."""
    return ChildError(msg, module, name, traceback, log, log_type, context)


def write_log_summary(out, log_type, log, last=None):
    errors, warnings = parse_log_events(log)
    nerr = len(errors)
    nwar = len(warnings)

    if nerr > 0:
        if last and nerr > last:
            errors = errors[-last:]
            nerr = last

        # If errors are found, only display errors
        out.write("\n%s found in %s log:\n" % (plural(nerr, "error"), log_type))
        out.write(make_log_context(errors))
    elif nwar > 0:
        if last and nwar > last:
            warnings = warnings[-last:]
            nwar = last

        # If no errors are found but warnings are, display warnings
        out.write("\n%s found in %s log:\n" % (plural(nwar, "warning"), log_type))
        out.write(make_log_context(warnings))


class ModuleChangePropagator:
    """Wrapper class to accept changes to a package.py Python module, and propagate them in the
    MRO of the package.

    It is mainly used as a substitute of the ``package.py`` module, when calling the
    "setup_dependent_package" function during build environment setup.
    """

    _PROTECTED_NAMES = ("package", "current_module", "modules_in_mro", "_set_attributes")

    def __init__(self, package: spack.package_base.PackageBase) -> None:
        self._set_self_attributes("package", package)
        self._set_self_attributes("current_module", package.module)

        #: Modules for the classes in the MRO up to PackageBase
        modules_in_mro = []
        for cls in package.__class__.__mro__:
            module = getattr(cls, "module", None)

            if module is None or module is spack.package_base:
                break

            if module is self.current_module:
                continue

            modules_in_mro.append(module)
        self._set_self_attributes("modules_in_mro", modules_in_mro)
        self._set_self_attributes("_set_attributes", {})

    def _set_self_attributes(self, key, value):
        super().__setattr__(key, value)

    def __getattr__(self, item):
        return getattr(self.current_module, item)

    def __setattr__(self, key, value):
        if key in ModuleChangePropagator._PROTECTED_NAMES:
            msg = f'Cannot set attribute "{key}" in ModuleMonkeyPatcher'
            return AttributeError(msg)

        setattr(self.current_module, key, value)
        self._set_attributes[key] = value

    def propagate_changes_to_mro(self):
        for module_in_mro in self.modules_in_mro:
            module_in_mro.__dict__.update(self._set_attributes)
