# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMendelianrandomization(RPackage):
    """Mendelian Randomization Package.

    Encodes several methods for performing Mendelian randomization analyses
    with summarized data. Summarized data on genetic associations with the
    exposure and with the outcome can be obtained from large consortia. These
    data can be used for obtaining causal estimates using instrumental variable
    methods."""

    cran = "MendelianRandomization"

    version("0.10.0", sha256="0851e91f826424f20fd4a58348ffe161d147bdc091d24d676e14d4cd6180e13c")
    version("0.7.0", sha256="cad7cc1b6964fc7d299864378694c5fd947caa83796a1958e581299796b854c7")

    depends_on("r@3.0.1:", type=("build", "run"))
    depends_on("r-knitr", type=("build", "run"))
    depends_on("r-rmarkdown", type=("build", "run"))
    depends_on("r-plotly@3.6.0:", type=("build", "run"))
    depends_on("r-ggplot2@1.0.1:", type=("build", "run"))
    depends_on("r-robustbase@0.92-6:", type=("build", "run"))
    depends_on("r-matrix@1.2:", type=("build", "run"))
    depends_on("r-iterpc@0.3:", type=("build", "run"))
    depends_on("r-quantreg@5.01:", type=("build", "run"))
    depends_on("r-rjson", type=("build", "run"))
    depends_on("r-glmnet", type=("build", "run"))
    depends_on("r-numderiv", type=("build", "run"), when="@0.10.0:")
    depends_on("r-rcpp", type=("build", "run"), when="@0.10.0:")
    depends_on("r-rcpparmadillo", type=("build", "run"), when="@0.10.0:")
