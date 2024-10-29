# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Optipng(AutotoolsPackage, SourceforgePackage):
    """
    OptiPNG is a PNG optimizer that recompresses image files to a smaller
    size, without losing any information. This program also converts external
    formats (BMP, GIF, PNM and TIFF) to optimized PNG, and performs PNG
    integrity checks and corrections.
    """

    homepage = "https://optipng.sourceforge.net/"
    sourceforge_mirror_path = "optipng/optipng-0.7.7.tar.gz"

    license("Zlib")

    version("0.7.8", sha256="25a3bd68481f21502ccaa0f4c13f84dcf6b20338e4c4e8c51f2cefbd8513398c")
    version("0.7.7", sha256="4f32f233cef870b3f95d3ad6428bfe4224ef34908f1b42b0badf858216654452")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # See https://github.com/imagemin/optipng-bin/issues/97    
    patch("for_aarch64_0.7.7.patch", when="@0.7.7")
    patch("for_aarch64_0.7.8.patch", when="@0.7.8:")
