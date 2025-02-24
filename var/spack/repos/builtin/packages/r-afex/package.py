# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAfex(RPackage):
    """Analysis of Factorial Experiments.

    Convenience functions for analyzing factorial experiments using ANOVA or
    mixed models. aov_ez(), aov_car(), and aov_4() allow specification of
    between, within (i.e., repeated-measures), or mixed (i.e., split-plot)
    ANOVAs for data in long format (i.e., one observation per row),
    automatically aggregating multiple observations per individual and cell of
    the design. mixed() fits mixed models using lme4::lmer() and computes
    p-values for all fixed effects using either Kenward-Roger or Satterthwaite
    approximation for degrees of freedom (LMM only), parametric bootstrap (LMMs
    and GLMMs), or likelihood ratio tests (LMMs and GLMMs).  afex_plot()
    provides a high-level interface for interaction or one-way plots using
    ggplot2, combining raw data and model estimates. afex uses type 3 sums of
    squares as default (imitating commercial statistical software)."""

    cran = "afex"

    license("GPL-2.0-or-later")

    version("1.3-1", sha256="4a64fb7e86e3d081e576c0d744d1613f391656082962c5799cf3fc5e2ca631a8")
    version("1.3-0", sha256="f8e276a1070288c54b83db1d1214fd88fe8d8b8698cf0c2743ef2a45f61e1933")
    version("1.2-1", sha256="e3a8cecd46db9521039275a5bf27937afb3ec4021644cc4fac94096cc585aacb")
    version("1.2-0", sha256="8b57ffb8ba2f6354185fc79c8b0cab2703d753b89a100f4325bb2e4c7a3531c2")
    version("1.1-1", sha256="66011599b193ebbb3bd241eb7200bd68ac4b5d2d1df84e63e9fdd72fb4110427")
    version("1.0-1", sha256="6febc34b87a1109f5cbcd213c08d2b7b3e9cf99065fa41c19bc88ac99fb104cc")
    version("0.28-1", sha256="cfb0b79bfa01b590afc3354a5b2ad3640d2f4974b036d6c256fa8e684bc69c2e")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-lme4@1.1-8:", type=("build", "run"))
    depends_on("r-pbkrtest@0.4-1:", type=("build", "run"))
    depends_on("r-lmertest@3.0-0:", type=("build", "run"))
    depends_on("r-car", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
