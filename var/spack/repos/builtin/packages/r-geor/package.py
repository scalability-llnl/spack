# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeor(RPackage):
    """Analysis of Geostatistical Data.

    Geostatistical analysis including variogram-based, likelihood-based and
    Bayesian methods. Software companion for Diggle and Ribeiro (2007)
    <doi:10.1007/978-0-387-48536-2>."""

    cran = "geoR"

    version("1.9-4", sha256="ae9d977cebe0f93b2593542f8d6d060467984dcf174e84ba632307c035d7ebbd")
    version("1.9-2", sha256="7ce3f5256a33a9de71b22a08caba634e77344889aac7d9eed02625a90254b9d9")
    version("1.8-1", sha256="990647804590b925a50f72897b24bbabd331cebef0be1696a60528b2f79d6fd3")
    version("1.7-5.2.1", sha256="3895e49c005a5745738d190ccaad43bb0aa49c74465d4d0b4dd88c5850ed63b9")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-sp", type=("build", "run"))
    depends_on("r-splancs", type=("build", "run"))
    depends_on("r-randomfields", type=("build", "run"), when="@:1.8-1")
