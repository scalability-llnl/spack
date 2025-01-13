# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRpart(RPackage):
    """Recursive Partitioning and Regression Trees.

    Recursive partitioning for classification, regression and survival trees.
    An implementation of most of the functionality of the 1984 book by Breiman,
    Friedman, Olshen and Stone."""

    cran = "rpart"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("4.1.23", sha256="f9b89aed6aa6cea656a2dcb271574e969ce2b1c98beb07bd91e17339f6daabaf")
    version("4.1.19", sha256="fe723ed0b5583fae8b40e6fecc29b357229cb11f2339b02a4e4f812926249565")
    version("4.1.16", sha256="27ec75258a5a3459ad999f5f36760ead974930744249605bf8465f234f31425c")
    version("4.1-15", sha256="2b8ebe0e9e11592debff893f93f5a44a6765abd0bd956b0eb1f70e9394cfae5c")
    version("4.1-13", sha256="8e11a6552224e0fbe23a85aba95acd21a0889a3fe48277f3d345de3147c7494c")
    version("4.1-11", sha256="38ab80959f59bcdd2c4c72860e8dd0deab0307668cbbf24f96014d7a2496ad98")
    version("4.1-10", sha256="c5ddaed288d38118876a94c7aa5000dce0070b8d736dba12de64a9cb04dc2d85")

    depends_on("r@2.15.0:", type=("build", "run"))
