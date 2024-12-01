# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeoquery(RPackage):
    """Get data from NCBI Gene Expression Omnibus (GEO).

    The NCBI Gene Expression Omnibus (GEO) is a public repository of
    microarray data. Given the rich and varied nature of this resource, it
    is only natural to want to apply BioConductor tools to these data.
    GEOquery is the bridge between GEO and BioConductor."""

    bioc = "GEOquery"

    license("MIT")

    version("2.68.0", commit="7995c579b068f98ebf3f1cd2cfd0575c3d73530c")
    version("2.66.0", commit="00a954e9f8223607b43cf112943ab575d03a0eb6")
    version("2.64.2", commit="e9b7f075a4a6a952660443ca93ed392d7a4fd6d7")
    version("2.62.2", commit="1966c108fe8a58ac39ef53c3c452fd160efa526e")
    version("2.58.0", commit="6332ca3791ddcfb233b9ad75b5904b3d60f49b93")
    version("2.52.0", commit="3059331eb82ad4947c2d1bef86ff9526e70af643")
    version("2.50.5", commit="135c17f8fe535acda14f95a37d1be1ff2bd80f97")
    version("2.48.0", commit="6a8d1ca195b5c26fb717ae93beb1a8d9b7031c5e")
    version("2.46.15", commit="a52b195ac640caae9679610d5b486b7cb828c0fd")
    version("2.42.0", commit="c26adef8d3ddbd6932a3170f2f84f6e4327641fb")

    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-readr", type=("build", "run"), when="@2.46.15:")
    depends_on("r-readr@1.3.1:", type=("build", "run"), when="@2.50.5:")
    depends_on("r-xml2", type=("build", "run"), when="@2.46.15:")
    depends_on("r-dplyr", type=("build", "run"), when="@2.46.15:")
    depends_on("r-data-table", type=("build", "run"), when="@2.62.2:")
    depends_on("r-tidyr", type=("build", "run"), when="@2.46.15:")
    depends_on("r-magrittr", type=("build", "run"), when="@2.46.15:")
    depends_on("r-limma", type=("build", "run"), when="@2.46.15:")
    depends_on("r-curl", type=("build", "run"), when="@2.64.2:")
    depends_on("r-r-utils", type=("build", "run"), when="@2.62.2:")

    depends_on("r-xml", type=("build", "run"), when="@2.42.0")
    depends_on("r-rcurl", type=("build", "run"), when="@2.42.0")
    depends_on("r-httr", type=("build", "run"), when="@:2.62.2")
