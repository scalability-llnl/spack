# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDplyr(RPackage):
    """A Grammar of Data Manipulation.

    A fast, consistent tool for working with data frame like objects, both in
    memory and out of memory."""

    cran = "dplyr"

    license("MIT")

    version("1.1.4", sha256="cf730414d5d4ab387b4e9890a4b1df9d17a3903488e8da8df1cf2e11e44558cb")
    version("1.1.2", sha256="c220c38a3a44977c43eeae3d9aef90e8bb297150cad0993ea8d3cc13150096e3")
    version("1.0.10", sha256="3ab639f627b4e439052df18f193f0ccab223225a4ae2ff8c18aba4f9807e0f2b")
    version("1.0.9", sha256="e2e1f7312618b4e32ada9a1da79cef32eaec12acd408c973a6b069c6be4fb46b")
    version("1.0.7", sha256="d2fe3aedbce02fdddce09a8a80f85f5918a9d1f15f792ad4a98f254959d7123d")
    version("1.0.3", sha256="28a1a9d87e99154d4d1542ef9da9fd70f869a173dc9709f4583a5770bae58441")
    version("0.8.3", sha256="68b4aac65a69ea6390e90991d9c7ce7a011a07e5db439d60cce911a078424c0c")
    version("0.8.2", sha256="e2b6d5b30d04d86f270374623da426541cee8e33ce446fcab6cd7862abf8e18b")
    version("0.7.7", sha256="0553db5a55f0e6f5d2d111e88422c6d26e9d54cb36b860ad2ca28e3826e3d4a4")
    version("0.7.6", sha256="d489cc8b53854ec30737bb7d39b331b67ca35f4275ad19e97420d7a247808330")
    version("0.7.5", sha256="2fbd8f316a59670076d43a0fe854654621941ee5f621ea5f0185a3f5daafda50")
    version("0.7.4", sha256="7b1fc90750fbb46483423da6721832c545d37b157f4f3355784a65e50fada8c2")
    version("0.7.3", sha256="ae67ed4f629a74485626b8291b5219b81ee6fc4c5fe5a077bfbdfeae59dee573")
    version("0.7.2", sha256="2262d1ad9fefd5c7d1030dea0edd6ffe5747b827cabe088cc915b0a09818eb4a")
    version("0.7.1", sha256="8c7573464b2a808f711f8977d0039e043318f93e47f2e80ba85b1f4ca09d12f4")
    version("0.7.0", sha256="27b3593c09da5e99c0c4fb19ea826edd2cab619f8aaefd0cfd2a4140a0bd9410")
    version("0.5.0", sha256="93d3b829f1c2d38e14a4f2fa7d6398fc6c1a9e4189b3e78bc38a0eb0e864454f")

    depends_on("r@3.1.2:", type=("build", "run"))
    depends_on("r@3.2.0:", type=("build", "run"), when="@0.8.1:")
    depends_on("r@3.3.0:", type=("build", "run"), when="@1.0.3:")
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.0.9:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-generics", type=("build", "run"), when="@1.0.3:")
    depends_on("r-glue@1.3.0:", type=("build", "run"))
    depends_on("r-glue@1.3.2:", type=("build", "run"), when="@1.0.3:")
    depends_on("r-lifecycle@0.2.0:", type=("build", "run"), when="@1.0.3:")
    depends_on("r-lifecycle@1.0.0:", type=("build", "run"), when="@1.0.5:")
    depends_on("r-lifecycle@1.0.1:", type=("build", "run"), when="@1.0.9:")
    depends_on("r-lifecycle@1.0.3:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-cli@3.4.0:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-magrittr@1.5:", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-rlang@0.4.0:", type=("build", "run"))
    depends_on("r-rlang@0.4.9:", type=("build", "run"), when="@1.0.3:")
    depends_on("r-rlang@0.4.10:", type=("build", "run"), when="@1.0.5:")
    depends_on("r-rlang@1.0.2:", type=("build", "run"), when="@1.0.9:")
    depends_on("r-rlang@1.1.0:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-tibble@2.0.0:", type=("build", "run"))
    depends_on("r-tibble@2.1.3:", type=("build", "run"), when="@1.0.3:")
    depends_on("r-tibble@3.2.0:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-tidyselect@0.2.5:", type=("build", "run"))
    depends_on("r-tidyselect@1.1.0:", type=("build", "run"), when="@1.0.3:")
    depends_on("r-tidyselect@1.1.1:", type=("build", "run"), when="@1.0.9:")
    depends_on("r-tidyselect@1.2.0:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-vctrs@0.3.5:", type=("build", "run"), when="@1.0.3:")
    depends_on("r-vctrs@0.4.1:", type=("build", "run"), when="@1.0.9:")
    depends_on("r-vctrs@0.6.0:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-vctrs@0.6.4:", type=("build", "run"), when="@1.1.4:")
    depends_on("r-pillar@1.5.1:", type=("build", "run"), when="@1.0.6:")
    depends_on("r-pillar@1.9.0:", type=("build", "run"), when="@1.1.2:")

    depends_on("r-assertthat@0.2.0:", type=("build", "run"), when="@:0.8.3")
    depends_on("r-bindrcpp@0.2.0:", type=("build", "run"), when="@:0.7.9")
    depends_on("r-pkgconfig", type=("build", "run"), when="@:0.8.3")
    depends_on("r-rcpp@1.0.1:", type=("build", "run"), when="@:0.8.3")
    depends_on("r-bh", type=("build", "run"), when="@:0.8.3")
    depends_on("r-plogr@0.2.0:", type=("build", "run"), when="@0.7.0:0.8.3")
    depends_on("r-ellipsis", type=("build", "run"), when="@1.0.3:1.0.9")
