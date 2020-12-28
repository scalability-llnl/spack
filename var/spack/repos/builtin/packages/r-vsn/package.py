# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVsn(RPackage):
    """Variance stabilization and calibration for microarray data.

       The package implements a method for normalising microarray intensities,
       and works for single- and multiple-color arrays. It can also be used for
       data from other technologies, as long as they have similar format. The
       method uses a robust variant of the maximum-likelihood estimator for an
       additive-multiplicative error model and affine calibration. The model
       incorporates data calibration step (a.k.a. normalization), a model for
       the dependence of the variance on the mean intensity and a variance
       stabilizing data transformation. Differences between transformed
       intensities are analogous to "normalized log-ratios". However, in
       contrast to the latter, their variance is independent of the mean, and
       they are usually more sensitive and specific in detecting differential
       transcription."""

    homepage = "https://bioconductor.org/packages/vsn"
    git      = "https://git.bioconductor.org/packages/vsn.git"

    version('3.52.0', commit='e80642d850ae93bc141654200a8970b561a94fbe')
    version('3.50.0', commit='ad49fcc288c6065d0f04040acd688e7f0d7d927e')
    version('3.48.1', commit='d57f64112004b1d73b3be625949830209de027eb')
    version('3.46.0', commit='7ecfd20452348da27d6fcc052cbff2b9be777792')
    version('3.44.0', commit='e54513fcdd07ccfb8094359e93cef145450f0ee0')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-hexbin', when='@3.44.0', type=('build', 'run'))

    depends_on('r@3.4.0:', when='@3.46.0:', type=('build', 'run'))
