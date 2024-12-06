# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Libsakura(CMakePackage):
    """High-performance, thread-safe library compatible with C and C++
    that is optimized for data analysis of astronomy and astrophysics.
    """

    homepage = "https://alma-intweb.mtk.nao.ac.jp/~sakura/api/html/index.html"
    url = "https://alma-dl.mtk.nao.ac.jp/ftp/sakura/releases/src/libsakura-4.0.2065/libsakura-4.0.2065.tar.gz"

    maintainers("mpokorny")

    license("LGPL-3.0-only")

    version("4.0.2065", sha256="3fde3713b1ca539f0b2397ec72a0086a3138ef63f89dce4be51ee60585df995f")
    version("3.0.2025", sha256="381a49d57cbc88dea15e08f7ed64ba57481d25bce8e5f68938dd4b6a30589c16")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8:", type="build")

    depends_on("eigen@3.2:")
    depends_on("fftw@3.3.2: precision=float", when="@:3")
    depends_on("fftw@3.3.2: precision=double", when="@4.0.0:")
    depends_on("log4cxx")

    patch("cmakelists.patch")

    def cmake_args(self):
        args = ["-DSIMD_ARCH=native", "-DBUILD_DOC:BOOL=OFF"]
        return args
