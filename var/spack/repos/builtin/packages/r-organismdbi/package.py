# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROrganismdbi(RPackage):
    """Software to enable the smooth interfacing of different database
       packages.

       The package enables a simple unified interface to several annotation
       packages each of which has its own schema by taking advantage of the
       fact that each of these packages implements a select methods."""

    homepage = "https://bioconductor.org/packages/OrganismDbi"
    git      = "https://git.bioconductor.org/packages/OrganismDbi.git"

    version('1.26.0', commit='495b4a8f8264d06d827537d43b3c6cc705244bb5')
    version('1.24.0', commit='3428952dc0f267a01e256a1c0873656cfbfde7f8')
    version('1.22.0', commit='24e953eb3847222d8018103b79b9fc72483cc513')
    version('1.20.0', commit='d42e06a24777e5ffb966ad5addb4f46dfffa2269')
    version('1.18.1', commit='ba2d1237256805e935d9534a0c6f1ded07b42e95')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.15.10:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.33.15:', type=('build', 'run'))
    depends_on('r-genomicfeatures@1.23.31:', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocinstaller', when='@1.18.1:1.22.0', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-rbgl', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.25:', type=('build', 'run'))

    depends_on('r-genomicranges@1.31.13:', when='@1.22.0:', type=('build', 'run'))

    depends_on('r-biocmanager', when='@1.24.0:', type=('build', 'run'))
