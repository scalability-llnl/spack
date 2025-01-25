# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import cmake, meson
from spack.package import *


class Multicharge(CMakePackage, MesonPackage):
    """Electronegativity equilibration model for atomic partial charges"""

    homepage = "https://github.com/grimme-lab/multicharge"
    url = "https://github.com/grimme-lab/multicharge/releases/download/v0.0.0/multicharge-0.0.0.tar.xz"
    git = "https://github.com/grimme-lab/multicharge.git"

    maintainers("RMeli", "awvwgk")

    license("Apache-2.0", checked_by="RMeli")

    build_system("cmake", "meson", default="meson")

    version("0.3.0", sha256="e8f6615d445264798b12d2854e25c93938373dc149bb79e6eddd23fc4309749d")

    variant("openmp", default=True, description="Enable OpenMP support")

    depends_on("lapack")
    depends_on("mctc-lib build_system=cmake", when="build_system=cmake")
    depends_on("mctc-lib build_system=meson", when="build_system=meson")


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        args = [self.define_from_variant("WITH_OpenMP", "openmp")]
        return args


class MesonBuilder(meson.MesonBuilder):
    def meson_args(self):
        lapack = self.spec["lapack"].libs.names[0]
        if lapack == "lapack":
            lapack = "netlib"
        elif lapack.startswith("mkl"):
            lapack = "mkl"
        elif lapack != "openblas":
            lapack = "auto"

        return [
            "-Dopenmp={0}".format(str("+openmp" in self.spec).lower()),
            "-Dlapack={0}".format(lapack),
        ]
