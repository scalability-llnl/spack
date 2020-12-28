# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReadbitmap(RPackage):
    """Identifies and reads Windows BMP, JPEG, PNG, and TIFF format bitmap
    images. Identification defaults to the use of the magic number embedded in
    the file rather than the file extension. Reading of JPEG and PNG image
    depends on libjpg and libpng libraries. See file INSTALL for details if
    necessary."""

    homepage = "https://github.com/jefferis/readbitmap"
    url      = "https://cloud.r-project.org/src/contrib/readbitmap_0.1.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/readbitmap"

    version('0.1.5', sha256='737d7d585eb33de2c200da64d16781e3c9522400fe2af352e1460c6a402a0291')

    depends_on('r-bmp', type=('build', 'run'))
    depends_on('r-jpeg', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-tiff', type=('build', 'run'))

    depends_on('jpeg')
    depends_on('libpng')
