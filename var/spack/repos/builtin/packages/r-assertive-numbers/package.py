# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssertiveNumbers(RPackage):
    """Assertions to Check Properties of Numbers.

    A set of predicates and assertions for checking the properties of numbers.
    This is mainly for use by other package developers who want to include
    run-time testing features in their own packages. End-users will usually
    want to use assertive directly."""

    cran = "assertive.numbers"

    version("0.0-2", sha256="bae18c0b9e5b960a20636e127eb738ecd8a266e5fc29d8bc5ca712498cd68349")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-assertive-base@0.0-2:", type=("build", "run"))
