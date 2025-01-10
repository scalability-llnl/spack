# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAdephylo(RPackage):
    """Exploratory Analyses for the Phylogenetic Comparative Method.

    Multivariate tools to analyze comparative data, i.e. a phylogeny and some
    traits measured for each taxa."""

    cran = "adephylo"

    license("GPL-2.0-or-later")

    version("1.1-16", sha256="b5ce5de26bbe6e40ca0650650acac3f613e5170d0b14dc5d6e6bbe83c416ce58")
    version("1.1-13", sha256="2aa132fee9d0a14ac09b0a96af40ac332cb4e13c892908803c335aa7319ca76d")
    version("1.1-11", sha256="154bf2645eac4493b85877933b9445442524ca4891aefe4e80c294c398cff61a")

    depends_on("r-ade4@1.7-10:", type=("build", "run"))
    depends_on("r-phylobase", type=("build", "run"))
    depends_on("r-ape", type=("build", "run"))
    depends_on("r-adegenet", type=("build", "run"))
