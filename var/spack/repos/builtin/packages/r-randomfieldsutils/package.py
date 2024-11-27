# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRandomfieldsutils(RPackage):
    """Utilities for the Simulation and Analysis of Random Fields and Genetic
    Data.

    Various utilities are provided that might be used in spatial statistics and
    elsewhere. It delivers a method for solving linear equations that checks
    the sparsity of the matrix before any algorithm is used."""

    cran = "RandomFieldsUtils"

    version("1.2.5", sha256="8cc288ba0f234eedb20ac791c89e18bde15e1f690ce34a303ff91a45d7f84e2e")
    version("1.1.0", sha256="f472602fed449a505a2e5787ab8a6c8c1b764335980adaeeb7b1f24069124a9d")
    version("0.5.6", sha256="07f484443dffab53fb530e56f1e36e7a59e77768638555975587b6a1e619480b")
    version("0.5.3", sha256="ea823cba2e254a9f534efb4b772c0aeef2039ee9ef99744e077b969a87f8031d")
    version("0.5.1", sha256="a95aab4e2025c4247503ff513570a65aa3c8e63cb7ce2979c9317a2798dfaca2")

    depends_on("r@3.0:", type=("build", "run"))
