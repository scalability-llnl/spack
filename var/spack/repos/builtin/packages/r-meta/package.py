# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMeta(RPackage):
    """General Package for Meta-Analysis.

    User-friendly general package providing standard methods for meta-analysis
    and supporting Schwarzer, Carpenter, and Rücker
    <doi:10.1007/978-3-319-21416-0>, "Meta-Analysis with R" (2015): - common
    effect and random effects meta-analysis; - several plots (forest, funnel,
    Galbraith / radial, L'Abbe, Baujat, bubble); - three-level meta-analysis
    model; - generalised linear mixed model; - Hartung-Knapp method for random
    effects model; - Kenward-Roger method for random effects model; -
    prediction interval; - statistical tests for funnel plot asymmetry; -
    trim-and-fill method to evaluate bias in meta-analysis; - meta-regression;
    - cumulative meta-analysis and leave-one-out meta-analysis; - import data
    from 'RevMan 5'; - produce forest plot summarising several (subgroup)
    meta-analyses."""

    cran = "meta"

    license("GPL-2.0-or-later")

    version("7.0-0", sha256="d8ead9c94f0d2b42766b8ea8358f40d0641cdcc9c25ba4b9a5fff1a59497de7d")
    version("6.2-1", sha256="2c2a0d4d8f3b07211120b232a155e3e1312164ce18817e0d5693c8da5da1d6cc")
    version("6.2-0", sha256="8ec8fb412996bbe17d3ca073f15c191a77bad486b08f39d7b8c2d07360ad5781")

    depends_on("r@4.0.0:", type=("build", "run"))
    depends_on("r-compquadform", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"), when="@7.0-0:")
    depends_on("r-lme4", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"), when="@7.0-0:")
    depends_on("r-metadat", type=("build", "run"), when="@7.0-0:")
    depends_on("r-metafor@3.0-0:", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"), when="@7.0-0:")
    depends_on("r-readr", type=("build", "run"), when="@7.0-0:")
    depends_on("r-stringr", type=("build", "run"), when="@7.0-0:")
    depends_on("r-xml2", type=("build", "run"))
