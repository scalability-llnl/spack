# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAbadata(RPackage):
    """Averaged gene expression in human brain regions from Allen Brain Atlas.

    Provides the data for the gene expression enrichment analysis conducted
    in the package 'ABAEnrichment'. The package includes three datasets
    which are derived from the Allen Brain Atlas: (1) Gene expression data
    from Human Brain (adults) averaged across donors, (2) Gene expression
    data from the Developing Human Brain pooled into five age categories and
    averaged across donors and (3) a developmental effect score based on the
    Developing Human Brain expression data. All datasets are restricted to
    protein coding genes."""

    bioc = "ABAData"

    version("1.24.0", commit="c4c42701f995ab8d5ede7f36ff06650493c82e36")
    version("1.20.0", commit="c08a841ffb54d6555eb80b90a7a8afe7e48201b3")
    version("1.14.0", commit="ed7460e7d2948684db69dd4b4f8e135af50198bd")
    version("1.12.0", commit="9c2f0fbda75b06a0807bd714528915920899282d")
    version("1.10.0", commit="197edb2c3fc733c9e44dde2b9b86ecedcd2c5e1a")
    version("1.8.0", commit="181a4af1af349064eb432255970e925ae2564e1a")
    version("1.6.0", commit="517c18a3d1809dde0291eeb47dd2545c7cfcdabe")

    depends_on("r@3.2:", type=("build", "run"))
