# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPbkrtest(RPackage):
    """Parametric Bootstrap, Kenward-Roger and Satterthwaite Based Methods for
    Test in Mixed Models.

    Test in mixed effects models. Attention is on mixed effects models as
    implemented in the 'lme4' package. For linear mixed models, this package
    implements (1) a parametric bootstrap test, (2) a Kenward-Roger-typ
    modification of F-tests for linear mixed effects models and (3) a
    Satterthwaite-type modification of F-tests for linear mixed effects models.
    The package also implements a parametric bootstrap test for generalized
    linear mixed models.  The facilities of the package are documented in the
    paper by Halehoh and Hojsgaard, (2012, <doi:10.18637/jss.v059.i09>).
    Please see 'citation("pbkrtest")' for citation details."""

    cran = "pbkrtest"

    license("GPL-2.0-or-later")

    version("0.5.2", sha256="8e79adf035a0fcf3c82145ad55847497379e009f7be880ba3007ebeb2e69b6e3")
    version("0.5.1", sha256="b2a3452003d93890f122423b3f2487dcb6925440f5b8a05578509e98b6aec7c5")
    version("0.5-0.1", sha256="f56525488c6efe4a5cbf849bf9a82747041478605b166c29bad54e464e46f469")
    version("0.4-7", sha256="5cbb03ad2b2468720a5a610a0ebda48ac08119a34fca77810a85f554225c23ea")
    version("0.4-6", sha256="9d28b8916fea3ffec8d5958bb8c531279b1e273f21fdbeb2fcad6d7e300a9c01")
    version("0.4-4", sha256="a685392ef3fca0ddc2254f6cc9bba6bc22b298fa823359fc4515e64e753abd31")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.2.3:", type=("build", "run"), when="@0.4-6:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.5-0.1:")
    depends_on("r@4.1.0:", type=("build", "run"), when="@0.5.2:")
    depends_on("r-lme4@1.1-10:", type=("build", "run"))
    depends_on("r-lme4@1.1-31:", type=("build", "run"), when="@0.5.2:")
    depends_on("r-broom", type=("build", "run"), when="@0.5-0.1:")
    depends_on("r-dplyr", type=("build", "run"), when="@0.5-0.1:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-matrix@1.2.3:", type=("build", "run"))
    depends_on("r-numderiv", type=("build", "run"), when="@0.5-0.1:")
    depends_on("r-knitr", type=("build", "run"), when="@0.5-0.1:0.5.1")
    depends_on("r-magrittr", type=("build", "run"), when="@0.5-0.1:0.5.1")
