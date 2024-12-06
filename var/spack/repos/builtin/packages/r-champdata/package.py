# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RChampdata(RPackage):
    """Packages for ChAMP package.

    Provides datasets needed for ChAMP including a test dataset and blood
    controls for CNA analysis."""

    bioc = "ChAMPdata"

    version("2.32.0", commit="98a94978001b6a28543257e72a036c43d61e67ef")
    version("2.30.0", commit="6e05b8f7b004b1a5185ec4b387c32725e8bd95cb")
    version("2.28.0", commit="601555bf599828b6cfa125beffa51aebccdc8503")
    version("2.26.0", commit="ea7882707921af33eefab5133a1ccd4a409f045d")
    version("2.22.0", commit="eeedd4c477fac79f00743da8ff7da064221c5f3d")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r-genomicranges@1.22.4:", type=("build", "run"))
    depends_on("r-biocgenerics@0.16.1:", type=("build", "run"))
