# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Leptonica(CMakePackage):
    """Leptonica is an open source library containing software that is
    broadly useful for image processing and image analysis applications."""

    homepage = "http://www.leptonica.org/"
    url = "https://github.com/DanBloomberg/leptonica/archive/1.80.0.tar.gz"

    license("custom")

    version("1.84.1", sha256="ecd7a868403b3963c4e33623595d77f2c87667e2cfdd9b370f87729192061bef")
    version("1.83.1", sha256="4289d0a4224b614010072253531c0455a33a4d7c7a0017fe7825ed382290c0da")
    version("1.81.0", sha256="70ebc04ff8b9684205bd1d01843c635a8521255b74813bf7cce9a33368f7952c")
    version("1.80.0", sha256="3952b974ec057d24267aae48c54bca68ead8275604bf084a73a4b953ff79196e")
    version("1.79.0", sha256="bf9716f91a4844c2682a07ef21eaf68b6f1077af1f63f27c438394fd66218e17")
    version("1.78.0", sha256="f8ac4d93cc76b524c2c81d27850bfc342e68b91368aa7a1f7d69e34ce13adbb4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("giflib")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("zlib-api")
    depends_on("libwebp+libwebpmux+libwebpdemux")
    depends_on("openjpeg")

    def cmake_args(self):
        args = [self.define("BUILD_SHARED_LIBS", "ON")]

        return args
