# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTidyr(RPackage):
    """Tidy Messy Data.

    Tools to help to create tidy data, where each column is a variable, each
    row is an observation, and each cell contains a single value. 'tidyr'
    contains tools for changing the shape (pivoting) and hierarchy (nesting and
    'unnesting') of a dataset, turning deeply nested lists into rectangular
    data frames ('rectangling'), and extracting values out of string columns.
    It also includes tools for working with missing values (both implicit and
    explicit)."""

    cran = "tidyr"

    license("MIT")

    version("1.3.1", sha256="e820c261cb5543f572f49276a7bdc7302aa4215da4bf850b1b939a315353835d")
    version("1.3.0", sha256="8d532b9366fdd3ec9827b51830e559a49d073425007c766025f0e603964e0a9d")
    version("1.2.1", sha256="6971766d3663dc75c2328ab257816f4e42d9fdc05c2d87d171b8b9b5ecce61af")
    version("1.2.0", sha256="8cd01da9e97827521d01ea50b9225f2705c46b7538bbf74bec6249a04c1213a8")
    version("1.1.4", sha256="0b0c98be98a433e15a2550f60330b31a58529a9c58bc2abd7bff6462ab761241")
    version("1.1.2", sha256="08fccb67824515b33187886f3ca2cf2fe747a778514892dbbf5e565edf0dfd6c")
    version("0.8.3", sha256="a18f54ec35124110058ab23f7e0a3c037a8d50f0405520cf5cc5443ec022cc37")
    version("0.8.2", sha256="99a508d0539390364789c5f4835b36c4a383927f0ec1648e2a4636c1cc6e490f")
    version("0.7.2", sha256="062cea2e2b57fffd500e4ce31cba6d593e65684fc0897ea49ea38d257c76009c")
    version("0.5.1", sha256="dbab642ac7231cbfe3e2a0d4553fb4ffb3699c6d6b432be2bb5812dfbbdbdace")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r@3.6:", type=("build", "run"), when="@1.3.1:")
    depends_on("r-dplyr@0.7.0:", type=("build", "run"))
    depends_on("r-dplyr@0.8.2:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-dplyr@1.0.0:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-dplyr@1.0.10:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-glue", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@1.1.2:")
    depends_on("r-lifecycle@1.0.3:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-stringr@1.5.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-purrr@1.0.1:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-rlang@1.0.4:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-rlang@1.1.1:", type=("build", "run"), when="@1.3.1:")
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-tibble@2.1.1:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-tidyselect@0.2.5:", type=("build", "run"))
    depends_on("r-tidyselect@1.1.0:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-tidyselect@1.2.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-vctrs@0.3.0:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-vctrs@0.3.6:", type=("build", "run"), when="@1.1.3:")
    depends_on("r-vctrs@0.3.7:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-vctrs@0.5.2:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-cpp11@0.2.1:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-cpp11@0.2.6:", type=("build", "run"), when="@1.1.3:")
    depends_on("r-cpp11@0.4.0:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-cli@3.4.1:", type=("build", "run"), when="@1.3.0:")

    depends_on("r-stringi", type=("build", "run"), when="@:0.8.3")
    depends_on("r-rcpp", type=("build", "run"), when="@:0.8.3")
    depends_on("r-ellipsis@0.1.0:", type=("build", "run"), when="@1.1.2:1.2.1")
