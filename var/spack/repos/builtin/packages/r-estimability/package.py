# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REstimability(RPackage):
    """Tools for Assessing Estimability of Linear Predictions.

    Provides tools for determining estimability of linear functions of
    regression coefficients, and 'epredict' methods that handle non-estimable
    cases correctly. Estimability theory is discussed in many linear-models
    textbooks including Chapter 3 of Monahan, JF (2008), "A Primer on Linear
    Models", Chapman and Hall (ISBN 978-1-4200-6201-4)."""

    cran = "estimability"

    license("GPL-3.0-or-later")

    version("1.5.1", sha256="3ca6b96a39fd8877e8636f94d20f34308b7296c1376c646703d27df8591644e9")
    version("1.4.1", sha256="c65aaf1e452f3947013d3ce05ae674d48492081f615a942592dc91db780f1124")
    version("1.3", sha256="a33179c5fbd6a1a623d90cb6f1743148f92c09429fac466867f3ea70946a2e32")

    depends_on("r@4.1.0:", when="@1.5.1:", type=("build", "run"))
    depends_on("r@4.3.0:", when="@1.5:1.5.0", type=("build", "run"))
