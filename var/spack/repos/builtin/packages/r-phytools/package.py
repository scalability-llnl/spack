# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPhytools(RPackage):
    """Phylogenetic Tools for Comparative Biology (and Other Things)"""

    homepage = "http://github.com/liamrevell/phytools"
    url      = "https://cloud.r-project.org/src/contrib/phytools_0.6-60.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/phytools/"

    version('0.6-99', sha256='2ef532cba77c5f73803bd34582bef05709705311a0b50e42316e69944567390f')
    version('0.6-60', sha256='55cad759510d247ebbf03a53a46caddadd3bf87584ccf7fcd6dd06d44516b377')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-animation', type=('build', 'run'))
    depends_on('r-ape@4.0:', type=('build', 'run'))
    depends_on('r-clustergeneration', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-combinat', type=('build', 'run'))
    depends_on('r-expm', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-maps', type=('build', 'run'))
    depends_on('r-mnormt', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
    depends_on('r-phangorn@2.3.1:', type=('build', 'run'))
    depends_on('r-plotrix', type=('build', 'run'))
    depends_on('r-scatterplot3d', type=('build', 'run'))
    depends_on('r-gtools', when='@0.6-99:', type=('build', 'run'))
