# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMaldiquant(RPackage):
    """Quantitative Analysis of Mass Spectrometry Data.

    A complete analysis pipeline for matrix-assisted laser
    desorption/ionization-time-of-flight (MALDI-TOF) and other two-dimensional
    mass spectrometry data. In addition to commonly used plotting and
    processing methods it includes distinctive features, namely baseline
    subtraction methods such as morphological filters (TopHat) or the
    statistics-sensitive non-linear iterative peak-clipping algorithm (SNIP),
    peak alignment using warping functions, handling of replicated measurements
    as well as allowing spectra with different resolutions."""

    cran = "MALDIquant"

    version("1.22.3", sha256="fd094f0ea1a163ad1bd290e789ad827a76075d82ae5ce8a8e53a7095a7479383")
    version("1.22.1", sha256="0a52a55dbe76a7e7ca50c5555fea4381eeda0c215c66e420d8dc9bfd2992411c")
    version("1.21", sha256="0771f82034aa6a77af67f3572c900987b7e6b578d04d707c6e06689d021a2ff8")
    version("1.19.3", sha256="a730327c1f8d053d29e558636736b7b66d0671a009e0004720b869d2c76ff32c")
    version("1.19.2", sha256="8c6efc4ae4f1af4770b079db29743049f2fd597bcdefeaeb16f623be43ddeb87")
    version("1.16.4", sha256="9b910dbd5dd1a739a17a7ee3f83d7e1ebad2fee89fd01a5b274415d2b6d3b0de")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.21:")
