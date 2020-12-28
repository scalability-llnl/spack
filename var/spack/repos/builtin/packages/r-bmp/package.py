# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBmp(RPackage):
    """Reads Windows BMP format images. Currently limited to 8 bit greyscale
    images and 24,32 bit (A)RGB images. Pure R implementation without external
    dependencies."""

    homepage = "https://cloud.r-project.org/package=bmp"
    url      = "https://cloud.r-project.org/src/contrib/bmp_0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bmp"

    version('0.3', sha256='bdf790249b932e80bc3a188a288fef079d218856cf64ffb88428d915423ea649')
