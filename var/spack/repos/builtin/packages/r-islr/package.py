# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIslr(RPackage):
    """Data for an Introduction to Statistical Learning with Applications in R.

    We provide the collection of data-sets used in the book 'An Introduction to
    Statistical Learning with Applications in R'."""

    cran = "ISLR"

    version("1.4", sha256="7151c636808198ee759cbcf22f82a7aa76580fb8d11e4cd67f69f85401c820c3")
    version("1.2", sha256="b00f7a06d2fb646917e629cc2dbdab71c7de3eb17a8a4d06849901a299f1caad")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.4:")
