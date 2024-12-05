# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libimagequant(MakefilePackage):
    """Small, portable C library for high-quality conversion of RGBA images to
    8-bit indexed-color (palette) images.
    """

    homepage = "https://pngquant.org/lib/"
    url = "https://github.com/ImageOptim/libimagequant/archive/2.12.6.tar.gz"

    license("GPL-3.0-or-later")

    version("2.12.6", sha256="b34964512c0dbe550c5f1b394c246c42a988cd73b71a76c5838aa2b4a96e43a0")

    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        configure("--prefix=" + prefix)
