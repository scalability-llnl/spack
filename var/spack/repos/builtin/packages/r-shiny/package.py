# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RShiny(RPackage):
    """Web Application Framework for R.

    Makes it incredibly easy to build interactive web applications with R.
    Automatic "reactive" binding between inputs and outputs and extensive
    pre-built widgets make it possible to build beautiful, responsive, and
    powerful applications with minimal effort."""

    cran = "shiny"

    license("GPL-3.0-only OR custom")

    version("1.9.1", sha256="854b6a214f127d652de2e0e02d675fd53209b058c11911f56f8d41382ba654e3")
    version("1.8.1.1", sha256="a38d5fb5d750e2c2091ce9101f138c1f9bc7009bbb195227a3519c5d97e36753")
    version("1.7.4", sha256="bbfcdd7375013b8f59248b3f3f4e752acd445feb25179f3f7f65cd69614da4b5")
    version("1.7.3", sha256="b8ca9a39fa69ea9b270a7e9037198d95122c79bd493b865d909d343dd3523ada")
    version("1.7.2", sha256="23b5bfee8d597b4147e07c89391a735361cd9f69abeecfd9bd38a14d35fe6252")
    version("1.7.1", sha256="c03b2056fb41430352c7c0e812bcc8632e6ec4caef077d2f7633512d91721d00")
    version("1.5.0", sha256="23cb8bfa448389c256efdab75e7e8d3ff90e5de66264c4ab02df322fb4298e9e")
    version("1.3.2", sha256="28b851ae6c196ca845f6e815c1379247595ac123a4faa10a16533d1a9ce0c24f")
    version("1.0.5", sha256="20e25f3f72f3608a2151663f7836f2e0c6da32683a555d7541063ae7a935fa42")
    version("0.13.2", sha256="0fe7e952f468242d7c43ae49afcc764788f7f2fd5436d18c3d20a80db7296231")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r-httpuv@1.5.0:", type=("build", "run"))
    depends_on("r-httpuv@1.5.2:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-mime@0.3:", type=("build", "run"))
    depends_on("r-jsonlite@0.9.16:", type=("build", "run"))
    depends_on("r-xtable", type=("build", "run"))
    depends_on("r-fontawesome@0.2.1:", type=("build", "run"), when="@1.7.1:")
    depends_on("r-fontawesome@0.4.0:", type=("build", "run"), when="@1.7.3:")
    depends_on("r-htmltools@0.3.6:", type=("build", "run"))
    depends_on("r-htmltools@0.4.0.9003:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-htmltools@0.5.2:", type=("build", "run"), when="@1.7.1:")
    depends_on("r-htmltools@0.5.4:", type=("build", "run"), when="@1.7.4:")
    depends_on("r-r6@2.0:", type=("build", "run"))
    depends_on("r-sourcetools", type=("build", "run"))
    depends_on("r-later@0.7.2:", type=("build", "run"), when="@1.1.0:")
    depends_on("r-later@1.0.0:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-promises@1.0.1:", type=("build", "run"), when="@1.1.0:")
    depends_on("r-promises@1.1.0:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-crayon", type=("build", "run"), when="@1.1.0:")
    depends_on("r-rlang", type=("build", "run"), when="@1.1.0:")
    depends_on("r-rlang@0.4.0:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-rlang@0.4.10:", type=("build", "run"), when="@1.7.1:")
    depends_on("r-fastmap@1.0.0:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-fastmap@1.1.0:", type=("build", "run"), when="@1.7.1:")
    depends_on("r-fastmap@1.1.1:", type=("build", "run"), when="@1.7.5:")
    depends_on("r-withr", type=("build", "run"), when="@1.5.0:")
    depends_on("r-commonmark@1.7:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-glue@1.3.2:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-bslib@0.3.0:", type=("build", "run"), when="@1.7.1:")
    depends_on("r-bslib@0.6.0:", type=("build", "run"), when="@1.9.0:")
    depends_on("r-cachem", type=("build", "run"), when="@1.7.1:")
    depends_on("r-cachem@1.1.0:", type=("build", "run"), when="@1.9.0:")
    depends_on("r-lifecycle@0.2.0:", type=("build", "run"), when="@1.7.1:")

    depends_on("r-digest", type=("build", "run"), when="@:1.5.0")
    depends_on("r-ellipsis", type=("build", "run"), when="@1.7.1:1.8.0")
