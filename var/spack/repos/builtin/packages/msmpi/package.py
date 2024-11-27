# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

from spack.build_systems.generic import GenericBuilder
from spack.package import *


class Msmpi(Package):
    """MSMPI is a Windows port of MPICH provided by the Windows team"""

    homepage = "https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi"
    url = "https://github.com/microsoft/Microsoft-MPI/archive/refs/tags/v10.1.1.tar.gz"
    git = "https://github.com/microsoft/Microsoft-MPI.git"
    tags = ["windows"]

    executables = ["mpiexec"]

    version("10.1.1", sha256="63c7da941fc4ffb05a0f97bd54a67968c71f63389a0d162d3182eabba1beab3d")
    version("10.0.0", sha256="cfb53cf53c3cf0d4935ab58be13f013a0f7ccb1189109a5b8eea0fcfdcaef8c1")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    provides("mpi")

    depends_on("win-wdk")

    patch("ifort_compat.patch")

    requires("platform=windows")

    @classmethod
    def determine_version(cls, exe):
        # MSMPI is typically MS only, don't detect on other platforms
        # to avoid potential collisions with other mpiexec executables
        if sys.platform != "win32":
            return None
        output = Executable(exe)(output=str, error=str)
        ver_str = re.search(r"Microsoft MPI Startup Program \[Version ([0-9.]+)\]", output)
        return Version(ver_str.group(1)) if ver_str else None

    def setup_dependent_package(self, module, dependent_spec):
        # MSMPI does not vendor compiler wrappers, instead arguments should
        # be manually supplied to compiler by consuming package
        # Note: This is not typical of MPI installations
        dependent_module = dependent_spec.package.module
        self.spec.mpicc = dependent_module.spack_cc
        self.spec.mpicxx = dependent_module.spack_cxx
        self.spec.mpifc = dependent_module.spack_fc
        self.spec.mpif77 = dependent_module.spack_f77


class GenericBuilder(GenericBuilder):
    def setup_build_environment(self, env):
        ifort_root = os.path.join(*self.pkg.compiler.fc.split(os.path.sep)[:-2])
        env.set("SPACK_IFORT", ifort_root)

    def is_64bit(self):
        return "64" in str(self.pkg.spec.target.family)

    def build_command_line(self):
        args = ["-noLogo"]
        ifort_bin = self.pkg.compiler.fc
        if not ifort_bin:
            raise InstallError(
                "Cannot install MSMPI without fortran"
                "please select a compiler with fortran support."
            )
        args.append("/p:IFORT_BIN=%s" % os.path.dirname(ifort_bin))
        args.append("/p:VCToolsVersion=%s" % self.pkg.compiler.msvc_version)
        args.append("/p:WindowsTargetPlatformVersion=%s" % str(self.pkg.spec["wdk"].version))
        args.append("/p:PlatformToolset=%s" % self.pkg.compiler.cc_version)
        return args

    def install(self, spec, prefix):
        with working_dir(self.pkg.stage.build_directory, create=True):
            msbuild(*self.build_command_line())
