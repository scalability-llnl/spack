# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMetafor(RPackage):
    """Meta-Analysis Package for R.

    A comprehensive collection of functions for conducting meta-analyses in R.
    The package includes functions to calculate various effect sizes or outcome
    measures, fit equal-, fixed-, random-, and mixed-effects models to such
    data, carry out moderator and meta-regression analyses, and create various
    types of meta-analytical plots (e.g., forest, funnel, radial, L'Abbe,
    Baujat, bubble, and GOSH plots). For meta-analyses of binomial and
    person-time data, the package also provides functions that implement
    specialized methods, including the Mantel-Haenszel method, Peto's method,
    and a variety of suitable generalized linear (mixed-effects) models (i.e.,
    mixed-effects logistic and Poisson regression models). Finally, the package
    provides functionality for fitting meta-analytic multivariate/multilevel
    models that account for non-independent sampling errors and/or true effects
    (e.g., due to the inclusion of multiple treatment studies, multiple
    endpoints, or other forms of clustering). Network meta-analyses and
    meta-analyses accounting for known correlation structures (e.g., due to
    phylogenetic relatedness) can also be conducted. An introduction to the
    package can be found in Viechtbauer (2010) <doi:10.18637/jss.v036.i03>."""

    cran = "metafor"

    license("GPL-2.0-or-later")

    version("4.6-0", sha256="07344cc3bd87b8bd25ef998e9a6ce322ae8e448ef5af06ec3e79631724e18666")
    version("4.0-0", sha256="5cd552ebaf225b745c2e4d944ca80986dd1ad6f1a4c902fb646f3cb11b8dc23b")
    version("3.8-1", sha256="d694577f954144d8a5eeab6521fe1c87e68ddf9ecfd7ccc915d01533371b0514")

    depends_on("r@4.0.0:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-metadat", type=("build", "run"))
    depends_on("r-numderiv", type=("build", "run"), when="@4.0-0:")
    depends_on("r-nlme", type=("build", "run"))
    depends_on("r-mathjaxr", type=("build", "run"))
    depends_on("r-pbapply", type=("build", "run"))
