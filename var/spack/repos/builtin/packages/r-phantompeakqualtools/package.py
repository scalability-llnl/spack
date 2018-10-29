# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPhantompeakqualtools(RPackage):
    """Computes informative enrichment and quality measures for
       ChIP-seq/DNase-seq/FAIRE-seq/MNase-seq data. This is a modified version
       of r-spp to be used in conjunction with the phantompeakqualtools
       package."""

    homepage = "https://github.com/kundajelab/phantompeakqualtools"
    url      = "https://github.com/kundajelab/phantompeakqualtools/raw/master/spp_1.14.tar.gz"

    version('1.14', '4de207d570999170c1bf45bcba8c6d2d')

    depends_on('boost@1.41.0:')
    depends_on('r-catools', type=('build', 'run'))
    depends_on('r-snow', type=('build', 'run'))
    depends_on('r-snowfall', type=('build', 'run'))
    depends_on('r-bitops', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))

    conflicts('%gcc@6:')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('BOOST_ROOT', self.spec['boost'].prefix)
