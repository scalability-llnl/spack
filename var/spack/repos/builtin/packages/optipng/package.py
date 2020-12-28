# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    homepage = "http://optipng.sourceforge.net/"
    sourceforge_mirror_path = "optipng/optipng-0.7.7.tar.gz"

    version('0.7.7', sha256='4f32f233cef870b3f95d3ad6428bfe4224ef34908f1b42b0badf858216654452')
    # See https://github.com/imagemin/optipng-bin/issues/97
    patch('for_aarch64.patch', when='target=aarch64:')
