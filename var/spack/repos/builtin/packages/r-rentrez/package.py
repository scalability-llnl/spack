# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRentrez(RPackage):
    """'Entrez' in R.

    Provides an R interface to the NCBI's 'EUtils' API,
    allowing users to search databases like 'GenBank'
    <https://www.ncbi.nlm.nih.gov/genbank/> and 'PubMed'
    <https://pubmed.ncbi.nlm.nih.gov/>, process the
    results of those searches and pull data into their R sessions."""

    cran = "rentrez"

    version("1.2.3", sha256="fb256597ebe7780e38bef9c4c2626b3feacd60c7a5a29fc6a218cf0d8d132f74")

    depends_on("c", type="build")  # generated

    depends_on("r@2.6.0:", type=("build", "run"))
    depends_on("r-xml", type=("build", "run"))
    depends_on("r-httr@0.5:", type=("build", "run"))
    depends_on("r-jsonlite@0.9:", type=("build", "run"))
