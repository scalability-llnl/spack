# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Fckit(CMakePackage):
    """A Fortran toolkit for interoperating Fortran with C/C++."""

    homepage = "https://software.ecmwf.int/wiki/display/fckit"
    git = "https://github.com/ecmwf/fckit.git"
    url = "https://github.com/ecmwf/fckit/archive/0.9.0.tar.gz"

    maintainers("climbfuji")

    license("Apache-2.0")

    version("master", branch="master")
    version("develop", branch="develop")
    version("0.13.2", sha256="990623eb4eb999145f2d852da9fbd71a69e2e0be601c655c274e8382750dfda2")
    version("0.13.1", sha256="89a067a7b5b1f2c7909739b567bd43b69f8a2d91e8cbcbac58655fb2d861db51")
    version("0.11.0", sha256="846f5c369940c0a3d42cd12932f7d6155339e79218d149ebbfdd02e759dc86c5")
    version("0.10.1", sha256="9cde04fefa50624bf89068ab793cc2e9437c0cd1c271a41af7d54dbd37c306be")
    version("0.10.0", sha256="f16829f63a01cdef5e158ed2a51f6d4200b3fe6dce8f251af158141a1afe482b")
    version("0.9.5", sha256="183cd78e66d3283d9e6e8e9888d3145f453690a4509fb701b28d1ac6757db5de")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("python")
    depends_on("ecbuild", type=("build"))

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    variant("eckit", default=True, description="Enable eckit")
    depends_on("eckit@:1.23 +mpi", when="@:0.10 +eckit")
    depends_on("eckit@1.24: +mpi", when="@0.11: +eckit")

    variant("openmp", default=True, description="Use OpenMP?")
    depends_on("llvm-openmp", when="+openmp %apple-clang", type=("build", "run"))
    variant("shared", default=True, description="Build shared libraries")
    variant("fismahigh", default=False, description="Apply patching for FISMA-high compliance")

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_ECKIT", "eckit"),
            self.define_from_variant("ENABLE_OMP", "openmp"),
            "-DFYPP_NO_LINE_NUMBERING=ON",
        ]

        if self.spec.satisfies("~shared"):
            args.append("-DBUILD_SHARED_LIBS=OFF")

        # Turn off finalization of derived data types (DDTs) because it is
        # flaky and we can't rely on fckit to auto-detect if the compiler
        # supports the feature or not.
        # https://github.com/JCSDA/spack-stack/issues/1521
        args.append("-DENABLE_FINAL=OFF")

        if (
            self.spec.satisfies("%intel")
            or self.spec.satisfies("%oneapi")
            or self.spec.satisfies("%gcc")
            or self.spec.satisfies("%nvhpc")
        ):
            cxxlib = "stdc++"
        elif self.spec.satisfies("%clang") or self.spec.satisfies("%apple-clang"):
            cxxlib = "c++"
        else:
            raise InstallError("C++ library not configured for compiler")
        args.append("-DECBUILD_CXX_IMPLICIT_LINK_LIBRARIES={}".format(cxxlib))

        return args

    @when("+fismahigh")
    def patch(self):
        patterns = ["tools/install-*", "tools/github-sha*", ".travis.yml"]
        for pattern in patterns:
            for path in glob.glob(pattern):
                os.remove(path)
