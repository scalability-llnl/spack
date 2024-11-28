# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Graphicsmagick(AutotoolsPackage):
    """GraphicsMagick is the swiss army knife of image processing.

    Provides a robust and efficient collection of tools and libraries which
    support reading, writing, and manipulating an image in over 88 major
    formats including important formats like DPX, GIF, JPEG, JPEG-2000, PNG,
    PDF, PNM, and TIFF.
    """

    homepage = "http://www.graphicsmagick.org/"
    url = "https://sourceforge.net/projects/graphicsmagick/files/graphicsmagick/1.3.29/GraphicsMagick-1.3.29.tar.xz/download"

    license("MIT")

    version("1.3.43", sha256="2b88580732cd7e409d9e22c6116238bef4ae06fcda11451bf33d259f9cbf399f")
    version("1.3.34", sha256="df009d5173ed0d6a0c6457234256c5a8aeaace782afa1cbab015d5a12bd4f7a4")
    version("1.3.33", sha256="130cb330a633580b5124eba5c125bbcbc484298423a97b9bed37ccd50d6dc778")
    version("1.3.32", sha256="b842a5a0d6c84fd6c5f161b5cd8e02bbd210b0c0b6728dd762b7c53062ba94e1")
    version("1.3.31", sha256="096bbb59d6f3abd32b562fc3b34ea90d88741dc5dd888731d61d17e100394278")
    version("1.3.30", sha256="d965e5c6559f55eec76c20231c095d4ae682ea0cbdd8453249ae8771405659f1")
    version("1.3.29", sha256="e18df46a6934c8c12bfe274d09f28b822f291877f9c81bd9a506f879a7610cd4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("bzip2")
    depends_on("ghostscript")
    depends_on("ghostscript-fonts")
    depends_on("graphviz")
    depends_on("jasper")
    depends_on("jpeg")
    depends_on("lcms")
    depends_on("libice")
    depends_on("libpng")
    depends_on("libsm")
    depends_on("libtiff")
    depends_on("libxml2")
    depends_on("xz")
    depends_on("zlib-api")

    def configure_args(self):
        args = ["--enable-shared"]
        return args
