# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tixi(CMakePackage):
    """TiXI is a fast and simple XML interface library and could be used
    from applications written in C, C++, Fortran, JAVA and Python. """

    homepage = "https://github.com/DLR-SC/tixi"
    url      = "https://github.com/DLR-SC/tixi/archive/v3.0.3.tar.gz"
    git      = "https://github.com/DLR-SC/tixi.git"

    version('3.0.3', sha256='3584e0cec6ab811d74fb311a9af0663736b1d7f11b81015fcb378efaf5ad3589')
    version('2.2.4', sha256='9080d2a617b7c411b9b4086de23998ce86e261b88075f38c73d3ce25da94b21c')

    depends_on('python', type='build')
    depends_on('expat')
    depends_on('curl')
    depends_on('libxml2')
    depends_on('libxslt')
