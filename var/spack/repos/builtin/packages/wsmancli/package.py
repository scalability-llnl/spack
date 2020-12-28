# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wsmancli(AutotoolsPackage):
    """Openwsman command line client"""

    homepage = "http://www.openwsman.org"
    url      = "https://github.com/Openwsman/wsmancli/archive/v2.6.0.tar.gz"

    version('2.6.0', sha256='766fef60d4c627d8b6129b3c9ae97d8676442bc6110b3a723610c54894365e0d')
    version('2.5.0', sha256='9e60e9b21d14328feadceeaf0c3c233d7ee701e7814010ede23367a9bd5efb33')
    version('2.3.2', sha256='b5ffd4c4cdbcde7cf8cf84be3a3c1b92d84ffb8b492e6008a83e090c760d6c2d')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('openwsman')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./bootstrap')
