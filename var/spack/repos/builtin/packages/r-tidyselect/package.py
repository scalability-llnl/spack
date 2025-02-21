# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTidyselect(RPackage):
    """Select from a Set of Strings.

    A backend for the selecting functions of the 'tidyverse'. It makes it easy
    to implement select-like functions in your own packages in a way that is
    consistent with other 'tidyverse' interfaces for selection."""

    cran = "tidyselect"

    license("MIT")

    version("1.2.1", sha256="169e97ba0bbfbcdf4a80534322751f87a04370310c40e27f04aac6525d45903c")
    version("1.2.0", sha256="538d26b727e37d618e2efd3b00836048f103112a03e6994bf07a02392e269e3b")
    version("1.1.2", sha256="0389a3b15417954a30d6d692f6ebdd3d0f318cb94a5c9b05365df2f4ea1d8270")
    version("1.1.1", sha256="18eb6a6746196a81ce19ee6cbf1db0c33f494177b97e2419312ef25a00ae486b")
    version("1.1.0", sha256="e635ed381fb53f7a53c3fa36bb33e134a3273d272367de2a8d909c821be93893")
    version("0.2.5", sha256="5ce2e86230fa35cfc09aa71dcdd6e05e1554a5739c863ca354d241bfccb86c74")
    version("0.2.4", sha256="5cb30e56ad5c1ac59786969edc8d542a7a1735a129a474f585a141aefe6a2295")
    version("0.2.3", sha256="0c193abc8251a60e1d2a32a99c77651c336bc185e3c2a72e5f8781813d181c2c")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.2:", type=("build", "run"), when="@1.1.0:")
    depends_on("r@3.4:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-glue@1.3.0:", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"), when="@1.2.0:")
    depends_on("r-lifecycle@1.0.3:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-rlang@0.2.2:", type=("build", "run"))
    depends_on("r-rlang@0.4.6:", type=("build", "run"), when="@1.1.0:")
    depends_on("r-rlang@1.0.1:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-rlang@1.0.4:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-vctrs@0.2.2:", type=("build", "run"), when="@1.1.0:")
    depends_on("r-vctrs@0.3.0:", type=("build", "run"), when="@1.1.1:")
    depends_on("r-vctrs@0.4.1:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-vctrs@0.5.2:", type=("build", "run"), when="@1.2.1:")

    depends_on("r-rcpp@0.12.0:", type=("build", "run"), when="@:0.2.5")
    depends_on("r-cli@3.3.0:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-ellipsis", type=("build", "run"), when="@1.1.0:1.1.2")

    depends_on("r-purrr", type=("build", "run"), when="@:1.1.2")
    depends_on("r-purrr@0.3.2:", type=("build", "run"), when="@1.1.0:1.1.2")
