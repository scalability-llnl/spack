# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OptionalDepTest(Package):
    """Description"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/optional_dep_test-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')
    version('1.1', '0123456789abcdef0123456789abcdef')

    variant('a',   default=False)
    variant('f',   default=False)
    variant('mpi', default=False)

    depends_on('a', when='+a')
    depends_on('b', when='@1.1')
    depends_on('c', when='%intel')
    depends_on('d', when='%intel@64.1')
    depends_on('e', when='%clang@34:40')

    depends_on('f', when='+f')
    depends_on('g', when='^f')
    depends_on('mpi', when='^g')

    depends_on('mpi', when='+mpi')
