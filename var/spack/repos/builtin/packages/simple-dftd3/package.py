# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SimpleDftd3(MesonPackage):
    """
    Simple reimplementation of the DFT-D3 dispersion correction
    """

    homepage = "https://dftd3.readthedocs.io"
    url = "https://github.com/dftd3/simple-dftd3/releases/download/v0.7.0/s-dftd3-0.7.0-source.tar.xz"
    git = "https://github.com/dftd3/simple-dftd3.git"

    maintainers("awvwgk")

    license("LGPL-3.0-or-later")

    version("main", branch="main")
    version("0.7.0", sha256="5390b20102474a3c37240f38226f3a54a809b34bcb910317bdd109b8c2865f4e")
    version("0.6.0", sha256="c057361565f570cb128489c70131487f71b6891a40e5292dfe37041596810dfe")
    version("0.5.1", sha256="0411fdaebe438f652a970cb232ae3199c4cc840366ed05fda4c38e634632040d")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=True, description="Use OpenMP parallelisation")
    variant("python", default=False, description="Build Python extension module")

    depends_on("mctc-lib")
    depends_on("meson@0.57.1:", type="build")  # mesonbuild/meson#8377
    depends_on("pkgconfig", type="build")
    depends_on("toml-f")
    depends_on("py-cffi", when="+python")
    depends_on("python@3.6:", when="+python")

    extends("python", when="+python")

    def meson_args(self):
        return [
            "-Dopenmp={0}".format(str("+openmp" in self.spec).lower()),
            "-Dpython={0}".format(str("+python" in self.spec).lower()),
        ]
