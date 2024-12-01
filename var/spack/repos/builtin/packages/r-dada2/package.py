# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDada2(RPackage):
    """Accurate sample inference from amplicon data with single nucleotide
    resolution"""

    homepage = "https://benjjneb.github.io/dada2/"
    url = "https://github.com/benjjneb/dada2/archive/v1.14.tar.gz"

    license("LGPL-3.0-only")

    version("1.20", sha256="351b80dc5cdd587f5d4fe2541574e3d0cf7966342ee913b47cb20c7eb150e3f5")
    version("1.14", sha256="19980b9d7b0a0e80e86010357cae11d1fc07c2d02067c4445169143cf1f99906")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.4:", type=("build", "run"))
    depends_on("r-rcpp@0.12.0:", type=("build", "run"))
    depends_on("r-biostrings@2.42.1:", type=("build", "run"))
    depends_on("r-ggplot2@2.1.0:", type=("build", "run"))
    depends_on("r-reshape2@1.4.1:", type=("build", "run"))
    depends_on("r-shortread@1.32.0:", type=("build", "run"))
    depends_on("r-rcppparallel@4.3.0:", type=("build", "run"))
    depends_on("r-iranges@2.6.0:", type=("build", "run"))
    depends_on("r-xvector@0.16.0:", type=("build", "run"))
    depends_on("r-biocgenerics@0.22.0:", type=("build", "run"))

    depends_on("gmake", type="build")
