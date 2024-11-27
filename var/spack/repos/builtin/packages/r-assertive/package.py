# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssertive(RPackage):
    """Readable Check Functions to Ensure Code Integrity.

    Lots of predicates (is_* functions) to check the state of your variables,
    and assertions (assert_* functions) to throw errors if they aren't in the
    right form."""

    cran = "assertive"

    version("0.3-6", sha256="c403169e83c433b65e911f7fd640b378e2a4a4765a36063584b8458168a4ea0a")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-assertive-base@0.0-4:", type=("build", "run"))
    depends_on("r-assertive-properties@0.0-2:", type=("build", "run"))
    depends_on("r-assertive-types@0.0-2:", type=("build", "run"))
    depends_on("r-assertive-numbers", type=("build", "run"))
    depends_on("r-assertive-strings", type=("build", "run"))
    depends_on("r-assertive-datetimes", type=("build", "run"))
    depends_on("r-assertive-files", type=("build", "run"))
    depends_on("r-assertive-sets@0.0-2:", type=("build", "run"))
    depends_on("r-assertive-matrices", type=("build", "run"))
    depends_on("r-assertive-models", type=("build", "run"))
    depends_on("r-assertive-data", type=("build", "run"))
    depends_on("r-assertive-data-uk", type=("build", "run"))
    depends_on("r-assertive-data-us", type=("build", "run"))
    depends_on("r-assertive-reflection@0.0-2:", type=("build", "run"))
    depends_on("r-assertive-code", type=("build", "run"))
    depends_on("r-knitr", type=("build", "run"))
