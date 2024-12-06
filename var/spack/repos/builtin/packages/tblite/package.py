# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tblite(MesonPackage):
    """Light-weight tight-binding framework"""

    homepage = "https://tblite.readthedocs.io"
    url = "https://github.com/tblite/tblite/releases/download/v0.3.0/tblite-0.3.0.tar.xz"
    git = "https://github.com/tblite/tblite.git"

    maintainers("awvwgk")

    license("LGPL-3.0-or-later")

    version("0.3.0", sha256="46d77c120501ac55ed6a64dea8778d6593b26fb0653c591f8e8c985e35884f0a")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=True, description="Use OpenMP parallelisation")
    variant("python", default=False, description="Build Python extension module")

    depends_on("blas")
    depends_on("dftd4@3:")
    depends_on("lapack")
    depends_on("mctc-lib@0.3:")
    depends_on("meson@0.57.2:", type="build")  # mesonbuild/meson#8377
    depends_on("pkgconfig", type="build")
    depends_on("py-cffi", when="+python")
    depends_on("py-numpy", when="+python")
    depends_on("python@3.6:", when="+python")
    depends_on("simple-dftd3")
    depends_on("toml-f")

    extends("python", when="+python")

    def meson_args(self):
        lapack = self.spec["lapack"].libs.names[0]
        if lapack == "lapack":
            lapack = "netlib"
        elif lapack.startswith("mkl"):
            lapack = "mkl"
        elif lapack != "openblas":
            lapack = "auto"

        return [
            "-Dlapack={0}".format(lapack),
            "-Dopenmp={0}".format(str("+openmp" in self.spec).lower()),
            "-Dpython={0}".format(str("+python" in self.spec).lower()),
        ]
