# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RChampdata(RPackage):
    """Packages for ChAMP package.

    Provides datasets needed for ChAMP including a test dataset and blood
    controls for CNA analysis."""

    bioc = "ChAMPdata"

    version("2.38.0", commit="373fee54eda7048bbd4e5046c1fb4c33c4620397")
    version("2.36.0", commit="f3d7acf36c1613dd55dc51d3ec5d23633c71b662")
    version("2.34.0", commit="debac652f0e001883c3c26b2f66efcea42ef633d")
    version("2.32.0", commit="98a94978001b6a28543257e72a036c43d61e67ef")
    version("2.30.0", commit="6e05b8f7b004b1a5185ec4b387c32725e8bd95cb")
    version("2.28.0", commit="601555bf599828b6cfa125beffa51aebccdc8503")
    version("2.26.0", commit="ea7882707921af33eefab5133a1ccd4a409f045d")
    version("2.22.0", commit="eeedd4c477fac79f00743da8ff7da064221c5f3d")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r-genomicranges@1.22.4:", type=("build", "run"))
    depends_on("r-biocgenerics@0.16.1:", type=("build", "run"))
