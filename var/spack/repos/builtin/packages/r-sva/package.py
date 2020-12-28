# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSva(RPackage):
    """Surrogate Variable Analysis.

       The sva package contains functions for removing batch effects and other
       unwanted variation in high-throughput experiment. Specifically, the sva
       package contains functions for the identifying and building surrogate
       variables for high-dimensional data sets. Surrogate variables are
       covariates constructed directly from high-dimensional data (like gene
       expression/RNA sequencing/methylation/brain imaging data) that can be
       used in subsequent analyses to adjust for unknown, unmodeled, or latent
       sources of noise. The sva package can be used to remove artifacts in
       three ways: (1) identifying and estimating surrogate variables for
       unknown sources of variation in high-throughput experiments (Leek and
       Storey 2007 PLoS Genetics,2008 PNAS), (2) directly removing known batch
       effects using ComBat (Johnson et al. 2007 Biostatistics) and (3)
       removing batch effects with known control probes (Leek 2014 biorXiv).
       Removing batch effects and using surrogate variables in differential
       expression analysis have been shown to reduce dependence, stabilize
       error rate estimates, and improve reproducibility, see (Leek and Storey
       2007 PLoS Genetics, 2008 PNAS or Leek et al. 2011 Nat. Reviews
       Genetics)."""

    homepage = "https://bioconductor.org/packages/sva"
    git      = "https://git.bioconductor.org/packages/sva.git"

    version('3.32.1', commit='1b8286734d00533b49d9f1456b6523cc778bb744')
    version('3.30.1', commit='fdb98bc2299dc5213c62d83cb7c0b1c1b4912f0c')
    version('3.28.0', commit='dd4937229dbccd2f383a04d5237fe147a884728d')
    version('3.26.0', commit='3cc5e75413c35ed5511892f5c36a8b5cb454937e')
    version('3.24.4', commit='ed2ebb6e33374dc9ec50e6ea97cc1d9aef836c73')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
