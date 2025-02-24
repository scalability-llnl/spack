# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDmrcate(RPackage):
    """Methylation array and sequencing spatial analysis methods.

    De novo identification and extraction of differentially methylated regions
    (DMRs) from the human genome using Whole Genome Bisulfite Sequencing (WGBS)
    and Illumina Infinium Array (450K and EPIC) data. Provides functionality
    for filtering probes possibly confounded by SNPs and cross-hybridisation.
    Includes GRanges generation and plotting functions."""

    bioc = "DMRcate"

    version("3.2.0", commit="1f46517bcdea269a2c9726d1156495d6dd172067")
    version("3.0.0", commit="9cd77dedef76528990487b931ae0cc314423c3b9")
    version("2.16.0", commit="9e42d8c8eb26dbd2d36a70bf32be322062ecc850")
    version("2.14.0", commit="6e7bae0917001e7664f01c3f8d261f9fe28c2f4d")
    version("2.12.0", commit="560dd5067b05715631739d0fb58ef9cebdbf7078")
    version("2.10.0", commit="81e83701da5c55ac83d0e0b5e640a9d431f09551")
    version("2.8.5", commit="c65dc79a33a047c10932a98b3383709a6bcb8903")
    version("2.4.1", commit="bc6242a0291a9b997872f575a4417d38550c9550")

    depends_on("r@3.6.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@2.8.5:2.17.1")
    depends_on("r@4.3.0:", type=("build", "run"), when="@2.99.0:")
    depends_on("r-annotationhub", type=("build", "run"), when="@2.99.0:")
    depends_on("r-experimenthub", type=("build", "run"))
    depends_on("r-bsseq", type=("build", "run"))
    depends_on("r-genomeinfodb", type=("build", "run"))
    depends_on("r-limma", type=("build", "run"))
    depends_on("r-edger", type=("build", "run"))
    depends_on("r-dss", type=("build", "run"), when="@:2.17.1")
    depends_on("r-minfi", type=("build", "run"))
    depends_on("r-missmethyl", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-plyr", type=("build", "run"))
    depends_on("r-gviz", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-biomart", type=("build", "run"), when="@2.99.0:")
