# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dropwatch(AutotoolsPackage):
    """Dropwatch is a project I started in an effort to improve the
    ability for developers and system administrator to diagnose problems
    in the Linux Networking stack, specifically in our ability to
    diagnose where packets are getting dropped."""

    homepage = "https://github.com/nhorman/dropwatch"
    url      = "https://github.com/nhorman/dropwatch/archive/v1.5.3.tar.gz"

    version('1.5.3', sha256='b748b66a816c1f94531446c0451da5461a4a31b0949244bb867d741c6ac0148b')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('libnl')
    depends_on('libpcap')
    depends_on('binutils')
    depends_on('readline')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')
