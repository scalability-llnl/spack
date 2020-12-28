# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMaldiquant(RPackage):
    """A complete analysis pipeline for matrix-assisted laser
       desorption/ionization-time-of-flight (MALDI-TOF) and other
       two-dimensional mass spectrometry data. In addition to commonly used
       plotting and processing methods it includes distinctive features,
       namely baseline subtraction methods such as morphological filters
       (TopHat) or the statistics-sensitive non-linear iterative peak-clipping
       algorithm (SNIP), peak alignment using warping functions, handling of
       replicated measurements as well as allowing spectra with different
       resolutions."""

    homepage = "https://cloud.r-project.org/package=MALDIquant"
    url      = "https://cloud.r-project.org/src/contrib/MALDIquant_1.16.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/MALDIquant"

    version('1.19.3', sha256='a730327c1f8d053d29e558636736b7b66d0671a009e0004720b869d2c76ff32c')
    version('1.19.2', sha256='8c6efc4ae4f1af4770b079db29743049f2fd597bcdefeaeb16f623be43ddeb87')
    version('1.16.4', sha256='9b910dbd5dd1a739a17a7ee3f83d7e1ebad2fee89fd01a5b274415d2b6d3b0de')

    depends_on('r@3.2.0:', type=('build', 'run'))
