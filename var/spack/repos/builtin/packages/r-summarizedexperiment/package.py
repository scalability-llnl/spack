# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSummarizedexperiment(RPackage):
    """SummarizedExperiment container.

       The SummarizedExperiment container contains one or more assays, each
       represented by a matrix-like object of numeric or other mode. The rows
       typically represent genomic ranges of interest and the columns represent
       samples."""

    homepage = "https://bioconductor.org/packages/SummarizedExperiment"
    git      = "https://git.bioconductor.org/packages/SummarizedExperiment.git"

    version('1.18.2', commit='e22fafe')
    version('1.14.1', commit='2c68d99e11c7345e5ed388370822ea48395c64a4')
    version('1.12.0', commit='5f8416864636add121ec1d6737ebb89a42227fd7')
    version('1.10.1', commit='7ad2e991c8285bfc4b2e15b29d94cc86d07f8f2b')
    version('1.8.1', commit='9d8a29aa9c78bbc7dcc6472537e13fc0d11dc1f7')
    version('1.6.5', commit='ec69cd5cfbccaef148a9f6abdfb3e22e888695d0')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-genomicranges@1.27.22:', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-delayedarray@0.1.9:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-biocgenerics@0.15.3:', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.13:', type=('build', 'run'))
    depends_on('r-iranges@2.7.2:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.11.4:', type=('build', 'run'))

    depends_on('r-genomicranges@1.29.14:', when='@1.8.1:', type=('build', 'run'))
    depends_on('r-delayedarray@0.3.20:', when='@1.8.1:', type=('build', 'run'))
    depends_on('r-iranges@2.11.17:', when='@1.8.1:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.13.1:', when='@1.8.1:', type=('build', 'run'))

    depends_on('r-genomicranges@1.31.17:', when='@1.10.1:', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.25:', when='@1.10.1:', type=('build', 'run'))
    depends_on('r-iranges@2.13.16:', when='@1.10.1:', type=('build', 'run'))

    depends_on('r-genomicranges@1.33.6:', when='@1.12.0:', type=('build', 'run'))
