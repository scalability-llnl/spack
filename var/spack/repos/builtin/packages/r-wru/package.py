# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWru(RPackage):
    """Who are You? Bayesian Prediction of Racial Category Using Surname, First
    Name, Middle Name, and Geolocation

    Predicts individual race/ethnicity using surname, first name, middle name,
    geolocation, and other attributes, such as gender and age. The method
    utilizes Bayes' Rule (with optional measurement error correction) to compute
    the posterior probability of each racial category for any given individual.
    The package implements methods described in Imai and Khanna (2016)
    "Improving Ecological Inference by Predicting Individual Ethnicity from
    Voter Registration Records" Political Analysis <doi:10.1093/pan/mpw001>."""

    homepage = "https://github.com/kosukeimai/wru"
    cran = "wru"

    maintainers("jgaeb")

    license("GPL-3.0-or-later")

    version("3.0.3", sha256="8430fc83609cda110eb340d104d408d362110d15d23208e7f5213cfeeb4a13b5")
    version("1.0.1", sha256="80b3f54cb2de77ea005755a2de3acfb923a1d380c0dbd52bc4d3e3fcb1d6f1fc")
    version("1.0.0", sha256="4eae65644981d0b99d3610adf40340b3606f40e6cd578e76a745524ba927e417")
    version("0.1-12", sha256="896ef4718109ab9fee686f050a3269cbab1589ef2aff7a45fc11a67f7bb35a29")
    version("0.1-11", sha256="a6af1a7e822b4d45759525872df3aa704d2cd431b47e583052d67de89c9bdba3")
    version("0.1-10", sha256="9bd3946b5005e8a7b1ff3e217690d0c02264b51f854785e6699d2533dd8145eb")
    version("0.1-9", sha256="105dc4d785b6044fac68696688be9c234acfdcb2b598f97fdbec3d38831b3577")
    version("0.1-8", sha256="efa7960a389ecf4c3cb6527848e06ae7c1d0d7f0da3a48c66453920f8b8752f0")
    version("0.1-7", sha256="8962f09e92f4209d8e52c86eba50cd35e7c0265154e608256fd3b80362a16bbb")
    version("0.1-6", sha256="81b4fa397d1cb56ea7635e76d198ccbfccd4141484f1f28f25c7dac408bfeed2")
    version("0.1-5", sha256="2a9d656e371c6d55c425f8e31e388ce574b9527fa674a7a0e65844d5b9e983e1")
    version("0.1-4", sha256="d463553cd835f85042b7679a14cf935efa9406a1fb4a67513ab251df59d6bd58")
    version("0.1-3", sha256="4e676ddb2084499404932163c858ec7574e2596e3bcb8cfac93d829dbe6b820a")
    version("0.1-2", sha256="ce9e622c89439f51698fdbb3dbbed7b8dda5aee886de5747e09e70c9982cf881")
    version("0.1-1", sha256="9b4d665867803f8992f7d2bf809da290396a1c7070fd72bf0c66c6408e1a7180")
    version("0.0-2", sha256="4ad5a09a5663906ea546fd9169444a559643d87ac18115e88b538a9260d40d4d")
    version("0.0-1", sha256="604a3e0f04fa3b1c5ee13543c0e3841f5a050f784f561d7ed8576542a27584ae")

    depends_on("r@3.2.0:", type=("build", "run"), when="@0.0-1:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.0-10:")
    depends_on("r@4.1.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-cli", type=("build", "run"), when="@3.0.0:")
    depends_on("r-devtools", type=("build", "run"), when="@0.0-2:0.1-12")
    depends_on("r-devtools@1.10.0:", type=("build", "run"), when="@0.1-1:0.1-12")
    depends_on("r-dplyr", type=("build", "run"), when="@1.0.0:")
    depends_on("r-future", type=("build", "run"), when="@1.0.0:")
    depends_on("r-furrr", type=("build", "run"), when="@1.0.0:")
    depends_on("r-purrr", type=("build", "run"), when="@1.0.0:")
    depends_on("r-rcpp", type=("build", "run"), when="@1.0.0:")
    depends_on("r-rcpparmadillo", type=("build", "run"), when="@1.0.0:")
    depends_on("r-rlang", type=("build", "run"), when="@3.0.0:")
    depends_on("r-piggyback", type=("build", "run"), when="@1.0.0:")
    depends_on("r-piggyback@0.1.4:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-pl94171", type=("build", "run"), when="@1.0.0:")
    depends_on("r-tidyr", type=("build", "run"), when="@3.0.0:")
