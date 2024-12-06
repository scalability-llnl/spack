# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


def resource_for_ver(ver, sha256):
    resource(
        name="cmake",
        url=f"https://github.com/llvm/llvm-project/releases/download/llvmorg-{ver}/cmake-{ver}.src.tar.xz",
        sha256=sha256,
        when=f"@{ver}",
    )


class LlvmOpenmp(CMakePackage):
    """The OpenMP subproject of LLVM contains the components required to build
    an executable OpenMP program that are outside the compiler itself."""

    homepage = "https://openmp.llvm.org/"
    url = "https://github.com/llvm/llvm-project/releases/download/llvmorg-14.0.6/openmp-14.0.6.src.tar.xz"

    license("Apache-2.0")

    version("18.1.0", sha256="ef1cef885d463e4becf5e132a9175a540c6f4487334c0e86274a374ce7d0a092")
    resource_for_ver(
        "18.1.0", sha256="d367bf77a3707805168b0a7a7657c8571207fcae29c5890312642ee42b76c967"
    )
    version("17.0.6", sha256="74334cbb4dc8b73a768448a7561d5a3540404940b2267b1fb9813a6464b320de")
    resource_for_ver(
        "17.0.6", sha256="807f069c54dc20cb47b21c1f6acafdd9c649f3ae015609040d6182cab01140f4"
    )
    version("16.0.0", sha256="e30f69c6533157ec4399193ac6b158807610815accfbed98695d72074e4bedd0")
    resource_for_ver(
        "16.0.0", sha256="04e62ab7d0168688d9102680adf8eabe7b04275f333fe20eef8ab5a3a8ea9fcc"
    )
    version("14.0.6", sha256="4f731ff202add030d9d68d4c6daabd91d3aeed9812e6a5b4968815cfdff0eb1f")
    version("12.0.1", sha256="60fe79440eaa9ebf583a6ea7f81501310388c02754dbe7dc210776014d06b091")
    version("9.0.0", sha256="9979eb1133066376cc0be29d1682bc0b0e7fb541075b391061679111ae4d3b5b")
    version("8.0.0", sha256="f7b1705d2f16c4fc23d6531f67d2dd6fb78a077dd346b02fed64f4b8df65c9d5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("multicompat", default=True, description="Support the GNU OpenMP runtime interface.")

    depends_on("cmake@3.13.4:", when="@12:", type="build")
    depends_on("cmake@2.8:", type="build")
    depends_on("py-lit", type="test")
    depends_on("py-filecheck", type="test")

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@14"):
            return "openmp-{}.src".format(self.version)
        else:
            return "."

    def url_for_version(self, version):
        if version >= Version("9.0.1"):
            url = "https://github.com/llvm/llvm-project/releases/download/llvmorg-{0}/openmp-{0}.src.tar.xz"
        else:
            url = "https://releases.llvm.org/{0}/openmp-{0}.src.tar.xz"

        return url.format(version)

    @when("@16:")
    def patch(self):
        cmake_mod_dir = os.path.join(self.stage.source_path, f"cmake-{self.version}.src")
        if os.path.isdir(cmake_mod_dir):
            os.rename(cmake_mod_dir, os.path.join(self.stage.path, "cmake"))

    def cmake_args(self):
        cmake_args = []
        # Add optional support for both Intel and gcc compilers
        if self.spec.satisfies("+multicompat"):
            cmake_args.append("-DKMP_GOMP_COMPAT=1")
        return cmake_args

    @property
    def libs(self):
        return find_libraries("libomp", root=self.prefix, recursive=True)
