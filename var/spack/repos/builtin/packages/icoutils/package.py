# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Icoutils(AutotoolsPackage):
    """extract and convert Microsoft icon and cursor files."""

    homepage = "https://www.nongnu.org/icoutils"
    url      = "https://nongnu.askapache.com/icoutils/icoutils-0.32.3.tar.bz2"

    version('0.32.3', sha256='17abe02d043a253b68b47e3af69c9fc755b895db68fdc8811786125df564c6e0')
    version('0.32.2', sha256='e892affbdc19cb640b626b62608475073bbfa809dc0c9850f0713d22788711bd')
    version('0.32.1', sha256='a9ed0fdb93e35708d9d07d0433ee1d71e07683404fa8d6e9d8aaeb6506a13fbf')

    depends_on('libpng@1.0.0:')
    depends_on('perl@5.6:')
    depends_on('perl-libwww-perl@5.64:')
