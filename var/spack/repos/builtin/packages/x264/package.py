# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class X264(AutotoolsPackage):
    """Software library and application for encoding video streams"""

    homepage = "https://www.videolan.org/developers/x264.html"
    git = "https://code.videolan.org/videolan/x264.git"

    license("GPL-2.0-or-later")

    version("20240314", commit="585e01997f0c7e6d72c8ca466406d955c07de912")
    version("20210613", commit="5db6aa6cab1b146e07b60cc1736a01f21da01154")

    depends_on("c", type="build")  # generated

    depends_on("nasm")

    def configure_args(self):
        return ["--enable-shared", "--enable-pic"]
