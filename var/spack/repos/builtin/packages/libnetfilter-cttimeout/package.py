# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibnetfilterCttimeout(AutotoolsPackage):
    """Conntrack timeout policy library."""

    homepage = "https://github.com/vyos/libnetfilter-cttimeout/"
    url      = "https://github.com/vyos/libnetfilter-cttimeout/archive/VyOS_1.2-2019Q4.tar.gz"

    version('1.2-2019Q4', sha256='71cebdf07a578901b160a54199062a4b4cd445e14742e2c7badc0900d8ae56b6')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('libmnl')
