# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vegas2(Package):
    """"VEGAS2 is an extension that uses 1,000 Genomes data to model SNP
        correlations across the autosomes and chromosome X"""

    homepage = "https://vegas2.qimrberghofer.edu.au/"
    url      = "https://vegas2.qimrberghofer.edu.au/vegas2v2"

    version('2', '815d80b86e9e294f99332bb5181e897a', expand=False)

    depends_on('perl', type='run')
    depends_on('r', type='run')
    depends_on('plink')
    depends_on('r-mvtnorm', type='run')
    depends_on('r-corpcor', type='run')

    def url_for_version(self, version):
        url = 'https://vegas2.qimrberghofer.edu.au/vegas2v{0}'
        return url.format(version)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('vegas2v{0}'.format(self.version), prefix.bin)
