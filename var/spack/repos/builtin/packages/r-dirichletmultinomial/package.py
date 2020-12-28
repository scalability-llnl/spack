# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDirichletmultinomial(RPackage):
    """Dirichlet-Multinomial Mixture Model Machine Learning for Microbiome
       Data.

       Dirichlet-multinomial mixture models can be used to describe variability
       in microbial metagenomic data. This package is an interface to code
       originally made available by Holmes, Harris, and Quince, 2012, PLoS ONE
       7(2): 1-15, as discussed further in the man page for this package,
       ?DirichletMultinomial."""

    homepage = "https://bioconductor.org/packages/DirichletMultinomial"
    git      = "https://git.bioconductor.org/packages/DirichletMultinomial.git"

    version('1.26.0', commit='7daa84948020811bb8a27d2e633fccfdcdd1018f')
    version('1.24.1', commit='50195d9b1986852da29100e77f6f09df5d6e2a35')
    version('1.22.0', commit='5864f4298105d12f345f27df77ad13bae4061ca5')
    version('1.20.0', commit='251529f301da1482551142240aeb6baf8dab2272')
    version('1.18.0', commit='81ccc8d83b8ef84f5d3e877bc0a04233a0f63c51')

    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('gsl')
