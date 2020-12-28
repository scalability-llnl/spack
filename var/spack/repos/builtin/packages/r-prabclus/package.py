# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPrabclus(RPackage):
    """prabclus: Functions for Clustering of Presence-Absence, Abundance and
    Multilocus Genetic Data"""

    homepage = "http://www.homepages.ucl.ac.uk/~ucakche"
    url      = "https://cloud.r-project.org/src/contrib/prabclus_2.2-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/prabclus"

    version('2.3-1', sha256='ef3294767d43bc3f72478fdaf0d1f13c8de18881bf9040c9f1add68af808b3c0')
    version('2.2-7.1', sha256='2c5bf3bbb0d225e04c53bb0e11e9c2a6809f0e46d95b8f6dc14b9dd6a2452975')
    version('2.2-6', sha256='41792980e40ba18204fab92d85120dcd468860e2204e52fb42636c6f7aee5a62')

    depends_on('r@2.1.0:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
