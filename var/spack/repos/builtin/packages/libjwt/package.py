# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libjwt(AutotoolsPackage):
    """libjwt JSON Web Token C Library"""

    homepage = "https://github.com/benmcollins/libjwt"
    git      = "https://github.com/benmcollins/libjwt"
    url      = "https://github.com/benmcollins/libjwt/archive/v1.12.0.tar.gz"

    maintainers = ['bollig']

    version('1.12.0', sha256='eaf5d8b31d867c02dde767efa2cf494840885a415a3c9a62680bf870a4511bee')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('jansson')
