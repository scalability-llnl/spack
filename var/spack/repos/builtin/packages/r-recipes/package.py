# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRecipes(RPackage):
    """Preprocessing Tools to Create Design Matrices.

    An extensible framework to create and preprocess design matrices.  Recipes
    consist of one or more data manipulation and analysis "steps".  Statistical
    parameters for the steps can be estimated from an initial data set and then
    applied to other data sets. The resulting design matrices can then be used
    as inputs into statistical or machine learning models."""

    cran = "recipes"

    license("MIT")

    version("1.1.0", sha256="c5dc8876bc680272812bbb4be39a29464c42a7b773f8cc6d07ac4145f830206d")
    version("1.0.6", sha256="105e97127cdd6aaeb9fb3348e51a9c46e21fb8bcb734cb3bbd6dbdf2b6b2fc8f")
    version("1.0.2", sha256="1a7b5a9a2946fa34599935b6d93101ec559d8a901d49cc691972c75df8d5670e")
    version("1.0.1", sha256="9e3ae212413409bf41ec7d1a311586e12c0ca79943cef436707d041c57125bc9")
    version("0.2.0", sha256="3d0073e3eb98ac089a94bf8430f3c50915ff1f495d8e967c37baa6a0f6cea0a4")
    version("0.1.17", sha256="ed20ba0ea0165310e31864ed7d2e005a2a37b76c7913977fd124d8b567616d3d")
    version("0.1.15", sha256="808ad2f4d68ae03aa27332437f037597e9c1bebd65ed4ebfab1d243ea6022e76")
    version("0.1.6", sha256="51e0db72de171d58d13ad8ffcf1dea402ab8f82100d161722041b6fd014cbfd9")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@1.0.1:")
    depends_on("r@3.6:", type=("build", "run"), when="@1.1.0:")
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-dplyr@1.1.0:", type=("build", "run"), when="@1.0.6:")
    depends_on("r-cli", type=("build", "run"), when="@1.0.1:")
    depends_on("r-clock@0.6.1:", type=("build", "run"), when="@1.0.6:")
    depends_on("r-generics", type=("build", "run"))
    depends_on("r-generics@0.1.0:", type=("build", "run"), when="@0.1.15:")
    depends_on("r-generics@0.1.0.9000:", type=("build", "run"), when="@0.2.0:")
    depends_on("r-generics@0.1.2:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-glue", type=("build", "run"))
    depends_on("r-gower", type=("build", "run"))
    depends_on("r-hardhat@0.1.6.9001:", type=("build", "run"), when="@0.2.0:")
    depends_on("r-hardhat@1.2.0:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-hardhat@1.3.0:", type=("build", "run"), when="@1.0.6:")
    depends_on("r-hardhat@1.4.0:", type=("build", "run"), when="@1.1.0:")
    depends_on("r-ipred", type=("build", "run"))
    depends_on("r-ipred@0.9-12:", type=("build", "run"), when="@0.1.17:")
    depends_on("r-lifecycle", type=("build", "run"), when="@0.1.15:")
    depends_on("r-lifecycle@1.0.3:", type=("build", "run"), when="@1.0.2:")
    depends_on("r-lubridate", type=("build", "run"))
    depends_on("r-lubridate@1.8.0:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-purrr@0.2.3:", type=("build", "run"))
    depends_on("r-purrr@1.0.0:", type=("build", "run"), when="@1.0.6:")
    depends_on("r-rlang@0.4.0:", type=("build", "run"))
    depends_on("r-rlang@1.0.3:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-rlang@1.1.0:", type=("build", "run"), when="@1.0.9:")
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"))
    depends_on("r-tidyr@1.0.0:", type=("build", "run"), when="@0.1.15:")
    depends_on("r-tidyselect@0.2.5:", type=("build", "run"))
    depends_on("r-tidyselect@1.1.0:", type=("build", "run"), when="@0.1.15:")
    depends_on("r-tidyselect@1.1.2:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-tidyselect@1.2.0:", type=("build", "run"), when="@1.0.2:")
    depends_on("r-timedate", type=("build", "run"))
    depends_on("r-vctrs", type=("build", "run"), when="@0.1.17:")
    depends_on("r-vctrs@0.5.0:", type=("build", "run"), when="@1.0.6:")
    depends_on("r-withr", type=("build", "run"))

    depends_on("r-ellipsis", type=("build", "run"), when="@0.1.17:1.0.10")
