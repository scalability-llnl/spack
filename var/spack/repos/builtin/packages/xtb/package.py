# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xtb(MesonPackage):
    """Semiempirical extended tight binding program package"""

    homepage = "https://xtb-docs.readthedocs.org"
    url = "https://github.com/grimme-lab/xtb/releases/download/v6.6.0/xtb-6.6.0-source.tar.xz"

    maintainers("awvwgk")

    license("LGPL-3.0-only")

    version("6.6.0", sha256="8460113f2678dcb23220af17b734f1221af302f42126bb54e3ae356530933b85")
    version("6.5.1", sha256="0922205cc224fe79e28f3d75be4e10c03efa8f3f666aedec8346fed82b272cad")
    version("6.5.0", sha256="5f780656bf7b440a8e1f753a9a877401a7d497fb3160762f48bdefc8a9914976")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("blas")
    depends_on("lapack")
    depends_on("meson@0.57.2:", type="build")
    depends_on("mctc-lib")
    depends_on("pkgconfig", type="build")
    depends_on("tblite", when="+tblite")
    depends_on("test-drive", type="build")

    variant("openmp", default=True, description="Use OpenMP parallelisation")
    variant("tblite", default=True, when="@6.6.0:", description="Use tblite for xTB calculations")

    def meson_args(self):
        lapack = self.spec["lapack"].libs.names[0]
        if lapack.startswith("mkl"):
            lapack = "mkl"
        elif lapack != "openblas":
            lapack = "netlib"

        lapack_opt = "-Dlapack={0}" if self.version >= Version("6.6.0") else "-Dla_backend={0}"

        return [
            lapack_opt.format(lapack),
            "-Dopenmp={0}".format(str("+openmp" in self.spec).lower()),
        ]
