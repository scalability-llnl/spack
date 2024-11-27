# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenetics(RPackage):
    """Population Genetics.

    Classes and methods for handling genetic data. Includes classes to
    represent genotypes and haplotypes at single markers up to multiple markers
    on multiple chromosomes. Function include allele frequencies, flagging
    homo/heterozygotes, flagging carriers of certain alleles, estimating and
    testing for Hardy-Weinberg disequilibrium, estimating and testing for
    linkage disequilibrium, ..."""

    cran = "genetics"

    license("GPL-2.0-or-later")

    version("1.3.8.1.3", sha256="fef2c95f6a57f32b3cf4acf003480439462bb28297c501c617de307bfeee9252")
    version("1.3.8.1.2", sha256="30cb67de2e901578fd802deb7fbfea6c93024c9fb6ea66cad88430a3a2a51eec")

    depends_on("r-combinat", type=("build", "run"))
    depends_on("r-gdata", type=("build", "run"))
    depends_on("r-gtools", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-mvtnorm", type=("build", "run"))
