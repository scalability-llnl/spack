# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBmp(RPackage):
    """Read Windows Bitmap (BMP) Images.

    Reads Windows BMP format images. Currently limited to 8 bit greyscale
    images and 24,32 bit (A)RGB images. Pure R implementation without external
    dependencies."""

    cran = "bmp"

    license("GPL-2.0-or-later")

    version("0.3", sha256="bdf790249b932e80bc3a188a288fef079d218856cf64ffb88428d915423ea649")
