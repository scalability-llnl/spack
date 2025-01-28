# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDeseq2(RPackage):
    """Differential gene expression analysis based on the negative binomial
    distribution.

    Estimate variance-mean dependence in count data from high-throughput
    sequencing assays and test for differential expression based on a model
    using the negative binomial distribution."""

    bioc = "DESeq2"

    version("1.46.0", commit="4887eb42fa96fcc234118ead8ffd11032a8f08bb")
    version("1.44.0", commit="5facd3093468ce2e75a2b742b1533efee13e5818")
    version("1.42.0", commit="17a39b5296cb3d897f1e2a9aa4bebbdefb13b46a")
    version("1.40.0", commit="c4962c3b16546e552fbc1a712258e4e21ff44241")
    version("1.38.0", commit="0e059f425d4ce6a5203685a4ad434f15bbd6e211")
    version("1.36.0", commit="2800b78ae52c0600f7e603c54af59beed3a2ed17")
    version("1.34.0", commit="25d4f74be59548122ccfbe8687d30c0bae5cf49a")
    version("1.30.0", commit="f4b47b208ee26ab23fe65c345f907fcfe70b3f77")
    version("1.24.0", commit="3ce7fbbebac526b726a6f85178063d02eb0314bf")
    version("1.22.2", commit="3c6a89b61add635d6d468c7fa00192314f8ca4ce")
    version("1.20.0", commit="7e88ea5c5e68473824ce0af6e10f19e22374cb7c")
    version("1.18.1", commit="ef65091d46436af68915124b752f5e1cc55e93a7")
    version("1.16.1", commit="f41d9df2de25fb57054480e50bc208447a6d82fb")

    depends_on("cxx", type="build")  # generated

    depends_on("r-s4vectors@0.9.25:", type=("build", "run"))
    depends_on("r-s4vectors@0.23.18:", type=("build", "run"), when="@1.30.0:")
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-summarizedexperiment@1.1.6:", type=("build", "run"))
    depends_on("r-biocgenerics@0.7.5:", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"), when="@1.40.0:")
    depends_on("r-locfit", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
    depends_on("r-rcpparmadillo", type=("build", "run"))

    depends_on("r-hmisc", type=("build", "run"), when="@:1.30.0")
    depends_on("r-genefilter", type=("build", "run"), when="@:1.38.0")
    depends_on("r-geneplotter", type=("build", "run"), when="@:1.38.0")
