# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# flake8: noqa: F401
"""pkgkit is a set of useful build tools and directives for packages.

Everything in this module is automatically imported into Spack package files.
"""
import llnl.util.filesystem
from llnl.util.filesystem import *

from spack.package import Package, run_before, run_after, on_package_attributes
from spack.package import inject_flags, env_flags, build_system_flags
from spack.build_systems.makefile import MakefilePackage
from spack.build_systems.aspell_dict import AspellDictPackage
from spack.build_systems.autotools import AutotoolsPackage
from spack.build_systems.cmake import CMakePackage
from spack.build_systems.cuda import CudaPackage
from spack.build_systems.qmake import QMakePackage
from spack.build_systems.scons import SConsPackage
from spack.build_systems.waf import WafPackage
from spack.build_systems.octave import OctavePackage
from spack.build_systems.python import PythonPackage
from spack.build_systems.r import RPackage
from spack.build_systems.perl import PerlPackage
from spack.build_systems.intel import IntelPackage
from spack.build_systems.meson import MesonPackage
from spack.build_systems.dynamic_inheritance import DynamicInheritancePackage

from spack.mixins import filter_compiler_wrappers

from spack.version import Version, ver

from spack.spec import Spec

from spack.dependency import all_deptypes

from spack.multimethod import when

import spack.directives
from spack.directives import *

import spack.util.executable
from spack.util.executable import *

from spack.package import \
    install_dependency_symlinks, flatten_dependencies, \
    DependencyConflictError, InstallError, ExternalPackageError

from spack.variant import any_combination_of, auto_or_any_combination_of
from spack.variant import disjoint_sets
