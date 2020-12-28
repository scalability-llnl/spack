# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Biobambam2(AutotoolsPackage):
    """Tools for early stage alignment file processing"""

    homepage = "https://gitlab.com/german.tischler/biobambam2"
    url      = "https://gitlab.com/german.tischler/biobambam2/-/archive/2.0.177-release-20201112105453/biobambam2-2.0.177-release-20201112105453.tar.gz"

    version('2.0.177', sha256='ad0a418fb49a31996a105a1a275c0d1dfc8b84aa91d48fa1efb6ff4fe1e74181',
            url='https://gitlab.com/german.tischler/biobambam2/-/archive/2.0.177-release-20201112105453/biobambam2-2.0.177-release-20201112105453.tar.gz')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('libmaus2')

    def configure_args(self):
        args = ['--with-libmaus2={0}'.format(self.spec['libmaus2'].prefix)]
        return args
