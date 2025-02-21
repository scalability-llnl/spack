# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RParty(RPackage):
    """A Laboratory for Recursive Partytioning.

    A computational toolbox for recursive partitioning. The core of the package
    is ctree(), an implementation of conditional inference trees which embed
    tree-structured  regression models into a well defined theory of
    conditional inference procedures. This non-parametric class of regression
    trees is applicable to all kinds of regression problems, including nominal,
    ordinal, numeric, censored as well as multivariate response variables and
    arbitrary measurement scales of the covariates.  Based on conditional
    inference trees, cforest() provides an implementation of Breiman's random
    forests. The function mob() implements an algorithm for recursive
    partitioning based on parametric models (e.g. linear models, GLMs or
    survival regression) employing parameter instability tests for split
    selection. Extensible functionality for visualizing tree-structured
    regression models is available. The methods are described in Hothorn et al.
    (2006) <doi:10.1198/106186006X133933>, Zeileis et al. (2008)
    <doi:10.1198/106186008X319331> and  Strobl et al. (2007)
    <doi:10.1186/1471-2105-8-25>."""

    cran = "party"

    license("GPL-2.0-only")

    version("1.3-17", sha256="f0e076b1e743cf50274b57d3a69526461fac5e499fc33d73825f293076f27d4b")
    version("1.3-13", sha256="def05e7f0c59f1b1ecf0ab3929cff75ae8c2691aaf52292cad4371281b897e7b")
    version("1.3-11", sha256="3ea41a1775d40bc6d0bdf657b98d939d99f98925ac985a31c969735c56618c9c")
    version("1.3-10", sha256="e5892955f6ce662ade568e646d1d672c3ecbf5d4e74b4a887a353e6160f7b56a")
    version("1.3-9", sha256="29a1fefdb86369285ebf5d48ab51268a83e2011fb9d9f609a2250b5f0b169089")
    version("1.3-5", sha256="1c3a35d3fe56498361542b3782de2326561c14a8fa1b76f3c9f13beb1fd51364")
    version("1.3-3", sha256="9f72eea02d43a4cee105790ae7185b0478deb6011ab049cc9d31a0df3abf7ce9")
    version("1.3-2", sha256="9f350fa21114151c49bccc3d5f8536dbc5a608cfd88f60461c9805a4c630510b")
    version("1.1-2", sha256="c3632b4b02dc12ec949e2ee5b24004e4a4768b0bc9737432e9a85acbc2ed0e74")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r@3.0.0:", type=("build", "run"), when="@1.2-3:")
    depends_on("r-mvtnorm@1.0-2:", type=("build", "run"))
    depends_on("r-modeltools@0.2-21:", type=("build", "run"))
    depends_on("r-strucchange", type=("build", "run"))
    depends_on("r-survival@2.37-7:", type=("build", "run"))
    depends_on("r-coin@1.1-0:", type=("build", "run"))
    depends_on("r-zoo", type=("build", "run"))
    depends_on("r-sandwich@1.1-1:", type=("build", "run"))
