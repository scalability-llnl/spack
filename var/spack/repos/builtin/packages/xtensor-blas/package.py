# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XtensorBlas(CMakePackage):
    """BLAS extension to xtensor"""

    homepage = "https://xtensor-stack.github.io"
    url = "https://github.com/xtensor-stack/xtensor-blas/archive/refs/tags/0.20.0.tar.gz"
    git = "git://github.com/xtensor-stack/xtensor-blas.git"

    license("BSD-3-Clause")

    version("develop", branch="master")
    version("0.20.0", sha256="272f5d99bb7511a616bfe41b13a000e63de46420f0b32a25fa4fb935b462c7ff")
    version("0.19.2", sha256="ef678c0e3f581cc8d61ea002c904c76513c8b0f798f9c9acaf980a835f9d09aa")
    version("0.19.1", sha256="c77cc4e2297ebd22d0d1c6e8d0a6cf0975176afa8cb99dbfd5fb2be625a0248f")
    version("0.19.0", sha256="0fa8001afa2d9f7fb1d3c101ae04565f39ef2880a84acec216e699ed14950cb4")
    version("0.18.0", sha256="fba992bc08323bc40fd04d6549e50e43b97942624a51e08129102d18c135eec0")
    version("0.17.2", sha256="2798c7e230d0c4b2d357bba20a0ef23a2b774d892be31ebbf702cb9935ea9f64")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build")
    # the information below can be found in the xtensor-blas README
    depends_on("xtensor@0.24.0:", when="@0.20:")
    depends_on("xtensor@0.23.3:", when="@0.19.1:0.19.2")
    depends_on("xtensor@0.23.0:", when="@0.19.0")
    depends_on("xtensor@0.22.0:", when="@0.18.0")
    depends_on("xtensor@0.21.4:", when="@0.17.2")
    depends_on("xtensor@0.21.2:", when="@:0.17.1")

    # C++14 support
    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.5")
