# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPmcmrplus(RPackage):
    """Calculate Pairwise Multiple Comparisons of Mean Rank Sums Extended.

    For one-way layout experiments the one-way ANOVA can be performed as an
    omnibus test. All-pairs multiple comparisons tests (Tukey-Kramer test,
    Scheffe test, LSD-test) and many-to-one tests (Dunnett test) for normally
    distributed residuals and equal within variance are available. Furthermore,
    all-pairs tests (Games-Howell test, Tamhane's T2 test, Dunnett T3 test,
    Ury-Wiggins-Hochberg test) and many-to-one (Tamhane-Dunnett Test) for
    normally distributed residuals and heterogeneous variances are provided.
    Van der Waerden's normal scores test for omnibus, all-pairs and many-to-one
    tests is provided for non-normally distributed residuals and homogeneous
    variances. The Kruskal-Wallis, BWS and Anderson-Darling omnibus test and
    all-pairs tests (Nemenyi test, Dunn test, Conover test,
    Dwass-Steele-Critchlow- Fligner test) as well as many-to-one (Nemenyi test,
    Dunn test, U-test) are given for the analysis of variance by ranks.
    Non-parametric trend tests (Jonckheere test, Cuzick test, Johnson-Mehrotra
    test, Spearman test) are included.  In addition, a Friedman-test for
    one-way ANOVA with repeated measures on ranks (CRBD) and Skillings-Mack
    test for unbalanced CRBD is provided with consequent all-pairs tests
    (Nemenyi test, Siegel test, Miller test, Conover test, Exact test) and
    many-to-one tests (Nemenyi test, Demsar test, Exact test).  A trend can be
    tested with Pages's test. Durbin's test for a two-way balanced incomplete
    block design (BIBD) is given in this package as well as Gore's test for
    CRBD with multiple observations per cell is given.  Outlier tests, Mandel's
    k- and h statistic as well as functions for Type I error and Power analysis
    as well as generic summary, print and plot methods are provided."""

    cran = "PMCMRplus"

    version("1.9.10", sha256="d883f897fa26a0bca0ba464dac7b360c6adee2c7867097e91fc7588030ed1f70")
    version("1.9.6", sha256="7f4791566d7dfaed0883187c52fbb845797ff6a1066e77667683ce96391b72d7")
    version("1.9.4", sha256="1ec36674bb6d2fac3a1b0889c4672e40849c7e3565ffb34bb73b61f973bba19a")
    version("1.9.3", sha256="76baba60f57343fa5bb6f6d2ea27aab77178e02b0d2f9d5d74abde7d18994f03")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-mvtnorm@1.0:", type=("build", "run"))
    depends_on("r-multcompview", type=("build", "run"))
    depends_on("r-gmp", type=("build", "run"))
    depends_on("r-rmpfr", type=("build", "run"))
    depends_on("r-suppdists", type=("build", "run"))
    depends_on("r-ksamples@1.2.7:", type=("build", "run"))
    depends_on("r-bwstest@0.2.1:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("gmp@4.2.3:")
    depends_on("mpfr@3.0.0:")
