# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRpostgres(RPackage):
    """'Rcpp' Interface to 'PostgreSQL'.

    Fully 'DBI'-compliant 'Rcpp'-backed interface to 'PostgreSQL'
    <https://www.postgresql.org/>, an open-source relational database."""

    cran = "RPostgres"

    version("1.4.7", sha256="3dd1f1d83bd8a25a0a86532c6971072fccea7b1769f601ad9daa8c9aa8f66924")
    version("1.4.5", sha256="70ff848cba51ddad4642a20e01cda1033e6f218b015a13380c30604bbd18c797")
    version("1.4.4", sha256="c9cc0648c432f837fd0eb4922db4903357244d5a2cedd04ea236f249b08acdfc")
    version("1.4.3", sha256="a5be494a54b6e989fadafdc6ee2dc5c4c15bb17bacea9ad540b175c693331be2")
    version("1.3.1", sha256="f68ab095567317ec32d3faa10e5bcac400aee5aeca8d7132260d4e90f82158ea")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-bit64", type=("build", "run"))
    depends_on("r-blob@1.2.0:", type=("build", "run"))
    depends_on("r-cpp11", type=("build", "run"), when="@1.4.6:")
    depends_on("r-dbi@1.1.0:", type=("build", "run"))
    depends_on("r-dbi@1.2.0:", type=("build", "run"), when="@1.4.7:")
    depends_on("r-hms@0.5.0:", type=("build", "run"))
    depends_on("r-hms@1.0.0:", type=("build", "run"), when="@1.4.3:")
    depends_on("r-lubridate", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"))
    depends_on("r-plogr@0.2.0:", type=("build", "run"))
    depends_on("postgresql@9.0:")

    depends_on("r-rcpp@0.11.4.2:", type=("build", "run"), when="@:1.4.5")
    depends_on("r-rcpp@1.0.7:", type=("build", "run"), when="@1.4.3:1.4.5")
    depends_on("r-bh", type=("build", "run"), when="@:1.3.1")
