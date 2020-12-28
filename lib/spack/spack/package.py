# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# flake8: noqa: F401
"""std is a set of useful build tools and directives for packages.

Everything in this module is automatically imported into Spack package files.
"""
import os
import shutil
from typing import List  # novm

import llnl.util.filesystem
from llnl.util.filesystem import (
    FileFilter,
    FileList,
    HeaderList,
    LibraryList,
    ancestor,
    can_access,
    change_sed_delimiter,
    copy_mode,
    filter_file,
    find,
    find_headers,
    find_all_headers,
    find_libraries,
    find_system_libraries,
    fix_darwin_install_name,
    force_remove,
    force_symlink,
    chgrp,
    chmod_x,
    copy,
    install,
    copy_tree,
    install_tree,
    is_exe,
    join_path,
    last_modification_time_recursive,
    mkdirp,
    partition_path,
    prefixes,
    remove_dead_links,
    remove_directory_contents,
    remove_if_dead_link,
    remove_linked_tree,
    set_executable,
    set_install_permissions,
    touch,
    touchp,
    traverse_tree,
    unset_executable_mode,
    working_dir,
)

import spack.config as _config
import spack.build_environment as _buildenv
from spack.package_base import (
    Package,
    BundlePackage,
    run_before,
    run_after,
    on_package_attributes,
)
from spack.package_base import inject_flags, env_flags, build_system_flags
from spack.build_systems.makefile import MakefilePackage
from spack.build_systems.aspell_dict import AspellDictPackage
from spack.build_systems.autotools import AutotoolsPackage
from spack.build_systems.cmake import CMakePackage
from spack.build_systems.cuda import CudaPackage
from spack.build_systems.oneapi import IntelOneApiPackage
from spack.build_systems.oneapi import IntelOneApiLibraryPackage
from spack.build_systems.rocm import ROCmPackage
from spack.build_systems.qmake import QMakePackage
from spack.build_systems.maven import MavenPackage
from spack.build_systems.scons import SConsPackage
from spack.build_systems.waf import WafPackage
from spack.build_systems.octave import OctavePackage
from spack.build_systems.python import PythonPackage
from spack.build_systems.r import RPackage
from spack.build_systems.perl import PerlPackage
from spack.build_systems.ruby import RubyPackage
from spack.build_systems.intel import IntelPackage
from spack.build_systems.meson import MesonPackage
from spack.build_systems.sip import SIPPackage
from spack.build_systems.gnu import GNUMirrorPackage
from spack.build_systems.sourceforge import SourceforgePackage
from spack.build_systems.sourceware import SourcewarePackage
from spack.build_systems.xorg import XorgPackage

from spack.mixins import filter_compiler_wrappers

from spack.version import Version, ver

from spack.spec import Spec, InvalidSpecDetected

from spack.dependency import all_deptypes

from spack.multimethod import when

import spack.directives
from spack.directives import (
    version,
    variant,
    conflicts,
    depends_on,
    extends,
    provides,
    patch,
    resource,
)

import spack.util.executable
from spack.util.executable import Executable, which, ProcessError

from spack.package_base import (
    install_dependency_symlinks,
    flatten_dependencies,
    DependencyConflictError,
)

from spack.installer import (
    ExternalPackageError,
    InstallError,
    InstallLockError,
    UpstreamPackageError,
)
from spack.install_test import get_escaped_text_output

from spack.variant import any_combination_of, auto_or_any_combination_of
from spack.variant import disjoint_sets

import multiprocessing as _mp
# TODO: make these build deps that can be installed if not found.
_jobs = _config.get("config:build_jobs", 16)
_jobs = min(_jobs, _mp.cpu_count())
make = _buildenv.MakeExecutable("make", _jobs)
gmake = _buildenv.MakeExecutable("gmake", _jobs)
scons = _buildenv.MakeExecutable("scons", _jobs)
ninja = _buildenv.MakeExecutable("ninja", _jobs)
make_jobs = _jobs

# easy shortcut to os.environ
env = os.environ

# Find the configure script in the archive path
# Don't use which for this; we want to find it in the current dir.
configure = _buildenv.Executable("./configure")

meson = _buildenv.Executable("meson")
cmake = _buildenv.Executable("cmake")
ctest = _buildenv.MakeExecutable("ctest", _jobs)

# fake lists
std_cmake_args = []  # type: List[str]
std_meson_args = []  # type: List[str]

# fake paths
spack_cc = ''
spack_cxx = ''
spack_f77 = ''
spack_fc = ''
prefix = ''
# Platform-specific library suffix.
dso_suffix = _buildenv.dso_suffix

# Emulate some shell commands for convenience
pwd = os.getcwd
cd = os.chdir
mkdir = os.mkdir
makedirs = os.makedirs
remove = os.remove
removedirs = os.removedirs
symlink = os.symlink

mkdirp = mkdirp
install = install
install_tree = install_tree
rmtree = shutil.rmtree
move = shutil.move

def static_to_shared_library(static_lib, shared_lib=None, **kwargs):
    raise NotImplementedError()
