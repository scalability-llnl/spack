# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OmptOpenmp(CMakePackage):
    """LLVM/Clang OpenMP runtime with OMPT support. This is a fork of the
    OpenMPToolsInterface/LLVM-openmp fork of the official LLVM OpenMP
    mirror.  This library provides a drop-in replacement of the OpenMP
    runtimes for GCC, Intel and LLVM/Clang.

    """

    homepage = "https://github.com/OpenMPToolsInterface/LLVM-openmp"
    url = "https://github.com/khuck/LLVM-openmp/archive/v0.1.tar.gz"

    license("MIT")

    version("0.1", sha256="a35dd2a83777fce54386d54cea8d2df9b5f34309d66fbc1d1757d55f6048c7a7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@2.8:", type="build")

    conflicts("%gcc@:4.7")

    root_cmakelists_dir = "runtime"

    @property
    def libs(self):
        return find_libraries("libomp", root=self.prefix, recursive=True)
