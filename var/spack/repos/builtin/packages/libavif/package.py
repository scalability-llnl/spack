# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libavif(CMakePackage):
    """libavif - Library for encoding and decoding .avif files."""

    homepage = "https://github.com/AOMediaCodec/libavif"
    url = "https://github.com/AOMediaCodec/libavif/archive/refs/tags/v1.1.1.tar.gz"

    license("bsd-2-clause")

    version("1.1.1", sha256="914662e16245e062ed73f90112fbb4548241300843a7772d8d441bb6859de45b")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.13:", type="build")

    def cmake_args(self):
        return [
            self.define("AVIF_JPEG", False),
            self.define("AVIF_LIBYUV", False),
            self.define("AVIF_ZLIBPNG", False),
        ]
