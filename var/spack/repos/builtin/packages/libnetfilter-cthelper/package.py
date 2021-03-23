# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibnetfilterCthelper(AutotoolsPackage):
    """Libnetfilter-cthelper library for user space helpers / ALGs"""

    homepage = "https://github.com/vyos/libnetfilter-cthelper/"
    url      = "https://github.com/vyos/libnetfilter-cthelper/archive/VyOS_1.2-2019Q4.tar.gz"

    version('1.2-2019Q4', sha256='15a7b13999d1428d75e720c8116318cd51bec1d365852ae1778d3c85b93a9777')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('libmnl')
