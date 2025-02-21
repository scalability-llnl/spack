# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBroomHelpers(RPackage):
    """Provides suite of functions to work with regression model 'broom::tidy()'
    tibbles. The suite includes functions to group regression model terms by
    variable, insert reference and header rows for categorical variables, add
    variable labels, and more."""

    homepage = "https://larmarange.github.io/broom.helpers/"
    cran = "broom.helpers"

    license("GPL-3.0-or-later", checked_by="wdconinc")

    version("1.16.0", sha256="9a7bac8678cdcc9a7e0f3b6d287d375fd5f1e880c916ac4d661f02c2c84e2715")

    depends_on("r@4.2:", type=("build", "run"), when="@1.16.0:")
    depends_on("r-broom@0.8:", type=("build", "run"))
    depends_on("r-cli", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-labelled", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-rlang@1.0.1:", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"))
