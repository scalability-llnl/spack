# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Form(AutotoolsPackage):
    """FORM is a Symbolic Manipulation System."""

    homepage = "https://www.nikhef.nl/~form/"
    url      = "https://github.com/vermaseren/form/archive/v4.2.1.tar.gz"

    version('4.2.1', sha256='6f32c7470d00e8ab6934dc352f5a78e29290146a00e5775f8cd5fef7810bbbb8')
    version('4.1-20131025', sha256='caece2c6e605ccf32eb3612c4ed5c9257a7a62824ad219c5e46b6d00066f1ba6')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('gmp', type='link')
    depends_on('zlib', type='link')

    def configure_args(self):
        args = ['--with-gmp=' + self.spec['gmp'].prefix,
                '--with-zlib=' + self.spec['zlib'].prefix]
        return args
