# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPopgenome(RPackage):
    """An Efficient Swiss Army Knife for Population Genomic Analyses.

    Provides efficient tools for population genomics data analysis, able to
    process individual loci, large sets of loci, or whole genomes. PopGenome
    <DOI:10.1093/molbev/msu136> not only  implements a wide range of population
    genetics statistics, but also facilitates the easy  implementation of new
    algorithms by other researchers. PopGenome is optimized for speed via  the
    seamless integration of C code."""

    cran = "PopGenome"

    version("2.7.5", sha256="d627b8ac87b4db6038d7349b2df20648d2fcfd48e2dafcd7f4731d1b607cbc75")
    version("2.7.1", sha256="a84903b151528fa026ccaba42ada22cd89babbc1824afd40269b7204e488a5fa")
    version("2.6.1", sha256="7a2922ed505fa801117a153e479d246bcf4854b91c6ab0241acc620a9d779b1c")

    depends_on("r@2.14.2:", type=("build", "run"))
    depends_on("r-ff", type=("build", "run"))
    depends_on("zlib-api")
