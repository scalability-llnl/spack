# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cmocka(CMakePackage):
    """Unit-testing framework in pure C"""
    homepage = "https://cmocka.org/"
    url      = "https://cmocka.org/files/1.1/cmocka-1.1.1.tar.xz"

    version('1.1.1', sha256='f02ef48a7039aa77191d525c5b1aee3f13286b77a13615d11bc1148753fc0389')
    version('1.1.0', sha256='e960d3bf1be618634a4b924f18bb4d6f20a825c109a8ad6d1af03913ba421330')

    depends_on('cmake@2.6.0:', type='build')

    parallel = False
