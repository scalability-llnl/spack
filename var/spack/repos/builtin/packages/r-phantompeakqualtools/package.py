# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
    url      = "https://github.com/hms-dbmi/spp/archive/refs/tags/1.15.2.tar.gz"

    version('1.15', sha256='172516b0f1f2a8132f22ab6fbfe41fb5943d675c2be02c733fcd5aa9651c6d22')
 
    depends_on('boost@1.41.0:')
    depends_on('r-catools', type=('build', 'run'))
    depends_on('r-snow', type=('build', 'run'))
    depends_on('r-snowfall', type=('build', 'run'))
    depends_on('r-bitops', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))

    def setup_build_environment(self, env):
        env.set('BOOST_ROOT', self.spec['boost'].prefix)
