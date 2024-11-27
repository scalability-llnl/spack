# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFpcompare(RPackage):
    """Reliable Comparison of Floating Point Numbers.

    Comparisons of floating point numbers are problematic due to errors
    associated with the binary representation of decimal numbers. Despite being
    aware of these problems, people still use numerical methods that fail to
    account for these and other rounding errors (this pitfall is the first to
    be highlighted in Circle 1 of Burns (2012) 'The R Inferno'
    <https://www.burns-stat.com/pages/Tutor/R_inferno.pdf>). This package
    provides new relational operators useful for performing floating point
    number comparisons with a set tolerance."""

    cran = "fpCompare"

    maintainers("dorton21")

    version("0.2.4", sha256="7189842a123e67b2d5d4b1dd72901959b821ec086d61cabc1dad9eae23f52570")
    version("0.2.3", sha256="f89be3568544a3a44e4f01b5050ed03705805308ec1aa4add9a5e1b5b328dbdf")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@0.2.4:")
