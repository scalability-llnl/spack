# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBsgenome(RPackage):
    """Software infrastructure for efficient representation of full genomes and
       their SNPs.

    Infrastructure shared by all the Biostrings-based genome data packages."""

    bioc = "BSgenome"

    version("1.68.0", commit="c546020750e900377fbdeae015a01a96d5962d09")
    version("1.66.1", commit="d1efdfa8e7242bc0f54cc1c3a9583ea555c924f6")
    version("1.64.0", commit="59cdebde613e9702985c003f699f4aea2b0f0e7b")
    version("1.62.0", commit="9b1859e11ffa082833f035a45274af6e4e83e863")
    version("1.58.0", commit="3a4926e03a7a1d7140a10c1b2bf6090808470145")
    version("1.52.0", commit="5398eba1cb56a873b29c04a7ce6858d5d60ff75b")
    version("1.50.0", commit="43910755f7477e4fe9bb968f186fddbb2f7355f9")
    version("1.48.0", commit="092a1b90482ace329cbd8ca2a338e91449acb93e")
    version("1.46.0", commit="bdfbd6d09820993585b8231ddea5e11c99008dc5")
    version("1.44.2", commit="105b00588a758d5ec7c347a7dff2756aea4516a0")

    depends_on("r@2.8.0:", type=("build", "run"))
    depends_on("r-biocgenerics@0.13.8:", type=("build", "run"))
    depends_on("r-s4vectors@0.9.36:", type=("build", "run"))
    depends_on("r-s4vectors@0.17.28:", type=("build", "run"), when="@1.48.0:")
    depends_on("r-iranges@2.1.33:", type=("build", "run"))
    depends_on("r-iranges@2.11.16:", type=("build", "run"), when="@1.46.0:")
    depends_on("r-iranges@2.13.16:", type=("build", "run"), when="@1.48.0:")
    depends_on("r-genomeinfodb@1.11.4:", type=("build", "run"))
    depends_on("r-genomeinfodb@1.13.1:", type=("build", "run"), when="@1.46.0:")
    depends_on("r-genomeinfodb@1.15.2:", type=("build", "run"), when="@1.48.0:")
    depends_on("r-genomeinfodb@1.25.6:", type=("build", "run"), when="@1.58.0:")
    depends_on("r-genomicranges@1.27.6:", type=("build", "run"))
    depends_on("r-genomicranges@1.29.14:", type=("build", "run"), when="@1.46.0:")
    depends_on("r-genomicranges@1.31.10:", type=("build", "run"), when="@1.48.0:")
    depends_on("r-biostrings@2.35.3:", type=("build", "run"))
    depends_on("r-biostrings@2.47.6:", type=("build", "run"), when="@1.48.0:")
    depends_on("r-rtracklayer@1.25.8:", type=("build", "run"))
    depends_on("r-rtracklayer@1.39.7:", type=("build", "run"), when="@1.48.0:")
    depends_on("r-matrixstats", type=("build", "run"), when="@1.58.0:")
    depends_on("r-xvector", type=("build", "run"))
    depends_on("r-xvector@0.29.3:", type=("build", "run"), when="@1.58.0:")
    depends_on("r-rsamtools", type=("build", "run"))
