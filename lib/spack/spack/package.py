# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# flake8: noqa: F401
"""spack.util.package is a set of useful build tools and directives for packages.

Everything in this module is automatically imported into Spack package files.
"""
from os import chdir, environ, getcwd, makedirs, mkdir, remove, removedirs
from shutil import move, rmtree

from spack.error import InstallError, NoHeadersError, NoLibrariesError

# Emulate some shell commands for convenience
env = environ
cd = chdir
pwd = getcwd

# import most common types used in packages
from typing import Dict, List, Optional

import llnl.util.filesystem
from llnl.util.filesystem import *
from llnl.util.symlink import symlink

import spack.util.executable

# These props will be overridden when the build env is set up.
from spack.build_environment import MakeExecutable
from spack.build_systems.aspell_dict import AspellDictPackage
from spack.build_systems.autotools import AutotoolsPackage
from spack.build_systems.bundle import BundlePackage
from spack.build_systems.cached_cmake import (
    CachedCMakePackage,
    cmake_cache_filepath,
    cmake_cache_option,
    cmake_cache_path,
    cmake_cache_string,
)
from spack.build_systems.cargo import CargoPackage
from spack.build_systems.cmake import CMakePackage, generator
from spack.build_systems.compiler import CompilerPackage
from spack.build_systems.cuda import CudaPackage
from spack.build_systems.generic import Package
from spack.build_systems.gnu import GNUMirrorPackage
from spack.build_systems.go import GoPackage
from spack.build_systems.intel import IntelPackage
from spack.build_systems.lua import LuaPackage
from spack.build_systems.makefile import MakefilePackage
from spack.build_systems.maven import MavenPackage
from spack.build_systems.meson import MesonPackage
from spack.build_systems.msbuild import MSBuildPackage
from spack.build_systems.nmake import NMakePackage
from spack.build_systems.octave import OctavePackage
from spack.build_systems.oneapi import (
    INTEL_MATH_LIBRARIES,
    IntelOneApiLibraryPackage,
    IntelOneApiLibraryPackageWithSdk,
    IntelOneApiPackage,
    IntelOneApiStaticLibraryList,
)
from spack.build_systems.perl import PerlPackage
from spack.build_systems.python import PythonExtension, PythonPackage
from spack.build_systems.qmake import QMakePackage
from spack.build_systems.r import RPackage
from spack.build_systems.racket import RacketPackage
from spack.build_systems.rocm import ROCmPackage
from spack.build_systems.ruby import RubyPackage
from spack.build_systems.scons import SConsPackage
from spack.build_systems.sip import SIPPackage
from spack.build_systems.sourceforge import SourceforgePackage
from spack.build_systems.sourceware import SourcewarePackage
from spack.build_systems.waf import WafPackage
from spack.build_systems.xorg import XorgPackage
from spack.builder import BaseBuilder
from spack.config import determine_number_of_jobs
from spack.deptypes import ALL_TYPES as all_deptypes
from spack.directives import *
from spack.install_test import (
    SkipTest,
    cache_extra_test_sources,
    check_outputs,
    find_required_file,
    get_escaped_text_output,
    install_test_root,
    test_part,
)
from spack.installer import ExternalPackageError, InstallLockError, UpstreamPackageError
from spack.mixins import filter_compiler_wrappers
from spack.multimethod import default_args, when
from spack.package_base import (
    DependencyConflictError,
    build_system_flags,
    env_flags,
    flatten_dependencies,
    inject_flags,
    install_dependency_symlinks,
    on_package_attributes,
)
from spack.package_completions import *
from spack.phase_callbacks import run_after, run_before
from spack.spec import InvalidSpecDetected, Spec
from spack.util.executable import *
from spack.util.filesystem import fix_darwin_install_name
from spack.variant import any_combination_of, auto_or_any_combination_of, disjoint_sets
from spack.version import Version, ver

# These are just here for editor support; they may be set when the build env is set up.
configure: Executable
make_jobs: int
make: MakeExecutable
ninja: MakeExecutable
python_include: str
python_platlib: str
python_purelib: str
python: Executable
spack_cc: str
spack_cxx: str
spack_f77: str
spack_fc: str
