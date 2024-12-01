# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mozjpeg(CMakePackage):
    """MozJPEG is a patched version of libjpeg-turbo which improves
    JPEG compression efficiency achieving higher visual quality and
    smaller file sizes at the same time"""

    homepage = "https://github.com/mozilla/mozjpeg"
    url = "https://github.com/mozilla/mozjpeg/archive/refs/tags/v4.1.1.tar.gz"

    maintainers("RemiLacroix-IDRIS")

    license("Zlib")

    version("4.1.1", sha256="66b1b8d6b55d263f35f27f55acaaa3234df2a401232de99b6d099e2bb0a9d196")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    provides("jpeg")

    variant("shared", default=True, description="Build shared libs")
    variant("static", default=True, description="Build static libs")
    variant("jpeg8", default=False, description="Emulate libjpeg v8 API/ABI")
    variant("png", default=False, description="Enable PNG support")

    # Can use either of these. But in the current version of the package
    # only nasm is used. In order to use yasm an environmental variable
    # NASM must be set.
    # TODO: Implement the selection between two supported assemblers.
    # depends_on("yasm", type="build")
    depends_on("nasm", type="build")
    depends_on("libpng@1.6:", when="+png")

    @property
    def libs(self):
        return find_libraries("libjpeg*", root=self.prefix, recursive=True)

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_SHARED", "shared"),
            self.define_from_variant("ENABLE_STATIC", "static"),
            self.define_from_variant("WITH_JPEG8", "jpeg8"),
            self.define_from_variant("PNG_SUPPORTED", "png"),
        ]

        return args
