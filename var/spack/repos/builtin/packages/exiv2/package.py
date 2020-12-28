# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exiv2(CMakePackage):
    """Exiv2 is a Cross-platform C++ library and a command line utility
    to manage image metadata
    """

    homepage = "https://www.exiv2.org/"
    url      = "https://github.com/Exiv2/exiv2/archive/v0.27.2.tar.gz"

    version('0.27.2', sha256='3dbcaf01fbc5b98d42f091d1ff0d4b6cd9750dc724de3d9c0d113948570b2934')

    depends_on('zlib', type='link')
    depends_on('expat@2.2.6:', type='link')
