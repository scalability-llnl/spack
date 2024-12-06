# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssertiveMatrices(RPackage):
    """Assertions to Check Properties of Matrices.

    A set of predicates and assertions for checking the properties of matrices.
    This is mainly for use by other package developers who want to include
    run-time testing features in their own packages. End-users will usually
    want to use assertive directly."""

    cran = "assertive.matrices"

    version("0.0-2", sha256="3462a7a7e11d7cc24180330d48cc3067cf92eab1699b3e4813deec66d99f5e9b")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-assertive-base@0.0-2:", type=("build", "run"))
