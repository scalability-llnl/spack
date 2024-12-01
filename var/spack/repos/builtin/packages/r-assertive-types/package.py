# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssertiveTypes(RPackage):
    """Assertions to Check Types of Variables.

    A set of predicates and assertions for checking the types of variables.
    This is mainly for use by other package developers who want to include
    run-time testing features in their own packages. End-users will usually
    want to use assertive directly."""

    cran = "assertive.types"

    version("0.0-3", sha256="ab6db2eb926e7bc885f2043fab679330aa336d07755375282d89bf9f9d0cb87f")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-assertive-base@0.0-7:", type=("build", "run"))
    depends_on("r-assertive-properties", type=("build", "run"))
    depends_on("r-codetools", type=("build", "run"))
