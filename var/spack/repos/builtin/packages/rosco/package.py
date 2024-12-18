# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rosco(CMakePackage):
    """
    ROSCO controls package for OpenFAST from NREL
    Note: this only builds ROSCO controls library for inclusion with OpenFAST
    If the toolbox or tuning scripts are needed, please build manually
    """

    homepage = "https://rosco.readthedocs.io/en/latest/"
    url = "https://github.com/NREL/ROSCO/archive/refs/tags/v2.9.0.tar.gz"
    git = "https://github.com/NREL/ROSCO.git"

    maintainers("dzalkind", "ndevelder")

    version("develop", branch="develop")
    version("main", branch="main")
    version("2.9.0", sha256="eb7f6220207b8a07c9570fb64bab591906b0c19d73ac4c24bb8dca252722ca79")
    version("2.8.0", sha256="7a2e3a7bebdf6ee73884a9e3502f904cc3a3f1aa1bf672c223ecbaa041bfc48f")
    version("2.7.0", sha256="b6a2cda92680cf6a460d194901a2f16c2635710a82788576a6383a3bb189fc83")
    version("2.6.0", sha256="ca1c1a6ac53e8220b107accccfb8b5299772c38b7c77cd8d2ba383e9825daeaa")
    version("2.5.1", sha256="55fe7bba612321baa6e089ee1156ef4db2e3bccf1b69534829b06f3367fff05d")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=False, description="Build shared libraries")
    variant("pic", default=False, description="Position independent code")

    patch("intel-oneapi-2x.patch", when="@2.5:2.8%oneapi")
    patch("intel-oneapi-29.patch", when="@2.9.0:2.9.1%oneapi")

    @property
    def root_cmakelists_dir(self):
        if self.spec.version >= Version("2.9.0"):
            return "rosco/controller"
        else:
            return "ROSCO"

    def cmake_args(self):
        options = []

        options.extend(
            [
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            ]
        )

        return options

    def setup_run_environment(self, env):
        env.set("ROSCO_DISCON", self.prefix.lib + "/libdiscon.so")
        env.set("ROSCO_DISCON_DIR", self.prefix.lib)

    def flag_handler(self, name, flags):
        if name == "fflags" and self.compiler.fc.endswith("gfortran"):
            flags.extend(["-ffree-line-length-0"])

        return (None, None, flags)
