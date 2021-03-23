# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dftd4(MesonPackage):
    """Generally Applicable Atomic-Charge Dependent London Dispersion Correction"""

    homepage = "https://www.chemie.uni-bonn.de/pctc/mulliken-center/software/dftd4"
    git = "https://github.com/dftd4/dftd4.git"

    version("main", branch="main")
    version("3.1.0", tag="v3.1.0")
    version("3.0.0", tag="v3.0.0")

    variant("openmp", default=True, description="Use OpenMP parallelisation")
    variant("python", default=False, description="Build Python extension module")

    depends_on("blas")
    depends_on("cmake", type="build")
    depends_on("lapack")
    depends_on("meson@0.57.1:", type="build")  # mesonbuild/meson#8377
    depends_on("pkg-config", type="build")
    depends_on("py-cffi", when="+python")
    depends_on("python@3.6:", when="+python")

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
