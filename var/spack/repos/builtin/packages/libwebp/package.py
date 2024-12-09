# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libwebp(AutotoolsPackage):
    """WebP is a modern image format that provides superior lossless and lossy
    compression for images on the web. Using WebP, webmasters and web
    developers can create smaller, richer images that make the web faster."""

    homepage = "https://developers.google.com/speed/webp/"
    url = "https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.0.3.tar.gz"

    license("BSD-3-Clause")

    version("1.4.0", sha256="61f873ec69e3be1b99535634340d5bde750b2e4447caa1db9f61be3fd49ab1e5")
    version("1.3.2", sha256="2a499607df669e40258e53d0ade8035ba4ec0175244869d1025d460562aa09b4")
    version("1.3.1", sha256="b3779627c2dfd31e3d8c4485962c2efe17785ef975e2be5c8c0c9e6cd3c4ef66")
    version("1.3.0", sha256="64ac4614db292ae8c5aa26de0295bf1623dbb3985054cb656c55e67431def17c")
    version("1.2.4", sha256="7bf5a8a28cc69bcfa8cb214f2c3095703c6b73ac5fba4d5480c205331d9494df")
    version("1.2.3", sha256="f5d7ab2390b06b8a934a4fc35784291b3885b557780d099bd32f09241f9d83f9")
    version("1.2.2", sha256="7656532f837af5f4cec3ff6bafe552c044dc39bf453587bd5b77450802f4aee6")
    version("1.2.0", sha256="2fc8bbde9f97f2ab403c0224fb9ca62b2e6852cbc519e91ceaa7c153ffd88a0c")
    version("1.0.3", sha256="e20a07865c8697bba00aebccc6f54912d6bc333bb4d604e6b07491c1a226b34f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("libwebpmux", default=False, description="Build libwebpmux")
    variant("libwebpdemux", default=False, description="Build libwebpdemux")
    variant("libwebpdecoder", default=False, description="Build libwebpdecoder")
    variant("libwebpextras", default=False, description="Build libwebpextras")
    variant("gif", default=False, description="GIF support")
    variant("jpeg", default=False, description="JPEG support")
    variant("png", default=False, description="PNG support")
    variant("tiff", default=False, description="TIFF support")

    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("giflib", when="+gif")
    depends_on("jpeg", when="+jpeg")
    depends_on("libpng", when="+png")
    depends_on("libtiff", when="+tiff")

    def configure_args(self):
        # TODO: add variants and dependencies for these
        args = ["--disable-gl", "--disable-sdl", "--disable-wic"]

        args += self.enable_or_disable("libwebpmux")
        args += self.enable_or_disable("libwebpdemux")
        args += self.enable_or_disable("libwebpdecoder")
        args += self.enable_or_disable("libwebpextras")
        args += self.enable_or_disable("gif")
        args += self.enable_or_disable("jpeg")
        args += self.enable_or_disable("png")
        args += self.enable_or_disable("tiff")

        return args
