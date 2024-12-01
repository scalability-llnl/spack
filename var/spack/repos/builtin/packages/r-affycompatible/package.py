# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffycompatible(RPackage):
    """Affymetrix GeneChip software compatibility.

    This package provides an interface to Affymetrix chip annotation and
    sample attribute files. The package allows an easy way for users to
    download and manage local data bases of Affynmetrix NetAffx annotation
    files. The package also provides access to GeneChip Operating System
    (GCOS) and GeneChip Command Console (AGCC)-compatible sample annotation
    files."""

    bioc = "AffyCompatible"

    version("1.58.0", commit="6508e72736371d353ec5f02d30caf8ffe39b342a")
    version("1.56.0", commit="37ea4bb885c791fb989f40092f3d0d2c57d35641")
    version("1.54.0", commit="fde7d86ccdb03c13c4838c18ac25477ffe6e0fe5")
    version("1.50.0", commit="3b12d12bd6d1a9f0d45e012817231d137d47089e")
    version("1.44.0", commit="98a27fbe880551fd32a5febb6c7bde0807eac476")
    version("1.42.0", commit="699303cc20f292591e2faa12e211c588efb9eaa8")
    version("1.40.0", commit="44838bdb5e8c26afbd898c49ed327ddd1a1d0301")
    version("1.38.0", commit="d47ee3a3a3d3bce11121e80fe02ee216b9199b12")
    version("1.36.0", commit="dbbfd43a54ae1de6173336683a9461084ebf38c3")

    depends_on("r@2.7.0:", type=("build", "run"))
    depends_on("r-xml@2.8-1:", type=("build", "run"))
    depends_on("r-rcurl@0.8-1:", type=("build", "run"))
    depends_on("r-biostrings", type=("build", "run"))
