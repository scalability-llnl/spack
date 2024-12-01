# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRstatix(RPackage):
    """Pipe-Friendly Framework for Basic Statistical Tests.

    Provides a simple and intuitive pipe-friendly framework, coherent with the
    'tidyverse' design philosophy, for performing basic statistical tests,
    including t-test, Wilcoxon test, ANOVA, Kruskal-Wallis and correlation
    analyses. The output of each test is automatically transformed into a tidy
    data frame to facilitate visualization. Additional functions are available
    for reshaping, reordering, manipulating and visualizing correlation matrix.
    Functions are also included to facilitate the analysis of factorial
    experiments, including purely 'within-Ss' designs (repeated measures),
    purely 'between-Ss' designs, and mixed 'within-and-between-Ss' designs.
    It's also possible to compute several effect size metrics, including "eta
    squared" for ANOVA, "Cohen's d" for t-test and 'Cramer V' for the
    association between categorical variables. The package contains helper
    functions for identifying univariate and multivariate outliers, assessing
    normality and homogeneity of variances."""

    cran = "rstatix"

    license("GPL-2.0-only")

    version("0.7.2", sha256="e0c6f5ab1d9c5d84713defabc5d149aad3d55944cffdb903cc128b694e5221a1")
    version("0.7.0", sha256="a5ae17dc32cc26fc5dcab9ff0a9747ce3786c9fe091699247ad8b9f823f2600c")
    version("0.6.0", sha256="ebb28e20c7e28809194a2a027bc83303b17be1e3db32f49325727c9279df9c5b")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-tidyr@1.0.0:", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-broom@0.5.6:", type=("build", "run"))
    depends_on("r-broom@0.7.4:", type=("build", "run"), when="@0.7.0:")
    depends_on("r-rlang@0.3.1:", type=("build", "run"))
    depends_on("r-tibble@2.1.3:", type=("build", "run"))
    depends_on("r-dplyr@0.7.1:", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-corrplot", type=("build", "run"))
    depends_on("r-tidyselect@1.0.0:", type=("build", "run"))
    depends_on("r-tidyselect@1.2.0:", type=("build", "run"), when="@0.7.2:")
    depends_on("r-car", type=("build", "run"))
    depends_on("r-generics@0.0.2:", type=("build", "run"))
