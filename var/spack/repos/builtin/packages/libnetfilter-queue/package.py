# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibnetfilterQueue(AutotoolsPackage):
    """Libnetfilter-queue libnetfilter queue library."""

    homepage = "https://github.com/vyos/libnetfilter-queue/"
    url      = "https://github.com/vyos/libnetfilter-queue/archive/VyOS_1.2-2019Q4.tar.gz"

    version('1.2-2019Q4', sha256='73b87e600b492cf9e3aa8fb6e9855e1ccc523a7bc466c1fd1a0e6ffa424d746e')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('libnfnetlink')
    depends_on('libmnl')
