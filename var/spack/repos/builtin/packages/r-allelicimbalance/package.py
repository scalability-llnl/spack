# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAllelicimbalance(RPackage):
    """Investigates Allele Specific Expression.

    Provides a framework for allelic specific expression investigation using
    RNA-seq data."""

    bioc = "AllelicImbalance"

    version("1.38.0", commit="75a3b0fefe635a0892eae338d0fdd4a9e091f957")
    version("1.36.0", commit="cb4910c1fd58cc4272c21251a8f120990e1aa431")
    version("1.34.0", commit="290708ccc4ceae1fbb9e9257cb254916449d389b")
    version("1.32.0", commit="428ab8c96bb15fab45e4084da25f98b01b9d60b6")
    version("1.28.0", commit="ac5d13c9ee0935bf9500ee542792644e752a1fde")
    version("1.22.0", commit="04692e367e8c6aac475d06adfd7cfa629baab05a")
    version("1.20.0", commit="4cd3a789d872151b0d906ec419677271fecdf7c3")
    version("1.18.0", commit="6d6eed7487e9207dba556bc76283bcc7745808ea")
    version("1.16.0", commit="85f652ae8a0dd15535819b6e934065182df5544a")
    version("1.14.0", commit="35958534945819baafde0e13d1eb4d05a514142c")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.28.0:")
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-genomicranges@1.31.8:", type=("build", "run"), when="@1.18.0:")
    depends_on("r-summarizedexperiment@0.2.0:", type=("build", "run"))
    depends_on("r-genomicalignments", type=("build", "run"))
    depends_on("r-genomicalignments@1.15.6:", type=("build", "run"), when="@1.18.0:")
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-bsgenome", type=("build", "run"))
    depends_on("r-bsgenome@1.47.3:", type=("build", "run"), when="@1.18.0:")
    depends_on("r-variantannotation", type=("build", "run"))
    depends_on("r-variantannotation@1.25.11:", type=("build", "run"), when="@1.18.0:")
    depends_on("r-biostrings", type=("build", "run"))
    depends_on("r-biostrings@2.47.6:", type=("build", "run"), when="@1.18.0:")
    depends_on("r-s4vectors@0.9.25:", type=("build", "run"))
    depends_on("r-s4vectors@0.17.25:", type=("build", "run"), when="@1.18.0:")
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-iranges@2.13.12:", type=("build", "run"), when="@1.18.0:")
    depends_on("r-rsamtools", type=("build", "run"))
    depends_on("r-rsamtools@1.31.2:", type=("build", "run"), when="@1.18.0:")
    depends_on("r-rsamtools@1.99.3:", type=("build", "run"), when="@1.22.0:")
    depends_on("r-genomicfeatures", type=("build", "run"))
    depends_on("r-genomicfeatures@1.31.3:", type=("build", "run"), when="@1.18.0:")
    depends_on("r-gviz", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-latticeextra", type=("build", "run"))
    depends_on("r-gridextra", type=("build", "run"))
    depends_on("r-seqinr", type=("build", "run"))
    depends_on("r-genomeinfodb", type=("build", "run"))
    depends_on("r-nlme", type=("build", "run"))
