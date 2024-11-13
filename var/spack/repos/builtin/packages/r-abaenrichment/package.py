# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAbaenrichment(RPackage):
    """Gene expression enrichment in human brain regions.

    The package ABAEnrichment is designed to test for enrichment of user
    defined candidate genes in the set of expressed genes in different human
    brain regions. The core function 'aba_enrich' integrates the expression
    of the candidate gene set (averaged across donors) and the structural
    information of the brain using an ontology, both provided by the Allen
    Brain Atlas project. 'aba_enrich' interfaces the ontology enrichment
    software FUNC to perform the statistical analyses. Additional functions
    provided in this package like 'get_expression' and 'plot_expression'
    facilitate exploring the expression data, and besides the standard
    candidate vs. background gene set enrichment, also three additional
    tests are implemented, e.g. for cases when genes are ranked instead of
    divided into candidate and background."""

    bioc = "ABAEnrichment"

    version("1.26.0", commit="33df9e162aec07e2aae92cc058cbfb33720ba4b4")
    version("1.24.0", commit="5d20752263ae8f18ea5f5a6cfbdd5921a0f236d7")
    version("1.20.0", commit="608433a0b07e6dd99915dc536a038d960f1be1d5")
    version("1.14.1", commit="e1ebfb5de816b924af16675a5ba9ed1a6b527b23")
    version("1.12.0", commit="1320e932deafd71d67c7a6f758d15b00d6d7f7d7")
    version("1.10.0", commit="15f33ccb694a91d2d2067c937682c4bc952def6c")
    version("1.8.0", commit="cb8155ee9a04fb55b2a2e8c23df7c0be15bb2624")
    version("1.6.0", commit="d2a0467dcb7aa6e103e3b83dccd6510b0e142ac1")

    depends_on("cxx", type="build")  # generated

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@1.8.0:")
    depends_on("r-rcpp@0.11.5:", type=("build", "run"))
    depends_on("r-gplots@2.14.2:", type=("build", "run"))
    depends_on("r-gtools@3.5.0:", type=("build", "run"))
    depends_on("r-abadata@0.99.2:", type=("build", "run"))
    depends_on("r-data-table@1.10.4:", type=("build", "run"), when="@1.8.0:")
    depends_on("r-gofuncr@1.1.2:", type=("build", "run"), when="@1.12.0:")
