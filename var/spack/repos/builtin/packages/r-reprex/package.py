# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReprex(RPackage):
    """Prepare Reproducible Example Code via the Clipboard.

    Convenience wrapper that uses the 'rmarkdown' package to render small
    snippets of code to target formats that include both code and output.  The
    goal is to encourage the sharing of small, reproducible, and runnable
    examples on code-oriented websites, such as <https://stackoverflow.com/>
    and <https://github.com>, or in email.  'reprex' also extracts clean,
    runnable R code from various common formats, such as copy/paste from an R
    session."""

    cran = "reprex"

    license("MIT")

    version("2.1.1", sha256="c860368cbc7ef90ea786fb61ab6fa42cd89b5258be48652abc20ad414001879c")
    version("2.0.2", sha256="a85b16e26112364a65c886efea050df08c17aadf1411fd14ec27d9ef13e87092")
    version("2.0.1", sha256="0e6d8667cacb63135476a766fba3a4f91e5ad86274ea66d2b1e6d773b5ca6426")
    version("0.3.0", sha256="203c2ae6343f6ff887e7a5a3f5d20bae465f6e8d9745c982479f5385f4effb6c")
    version("0.2.1", sha256="5d234ddfbcadc5a5194a58eb88973c51581e7e2e231f146974af8f42747b45f3")
    version("0.1.1", sha256="919ae93039b2d8fb8eace98da9376c031d734d9e75c237efb24d047f35b5ba4b")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.1:", type=("build", "run"), when="@0.2.0:")
    depends_on("r@3.3:", type=("build", "run"), when="@1:")
    depends_on("r@3.4:", type=("build", "run"), when="@2.0.2:")
    depends_on("r@3.6:", type=("build", "run"), when="@2.1.0:")
    depends_on("r-callr@2.0.0:", type=("build", "run"))
    depends_on("r-callr@3.3.1:", type=("build", "run"), when="@1:")
    depends_on("r-callr@3.6.0:", type=("build", "run"), when="@2:")
    depends_on("r-cli", type=("build", "run"), when="@1:")
    depends_on("r-cli@2.3.1:", type=("build", "run"), when="@2:")
    depends_on("r-cli@3.2.0:", type=("build", "run"), when="@2.0.2:")
    depends_on("r-clipr@0.4.0:", type=("build", "run"))
    depends_on("r-fs", type=("build", "run"), when="@0.2.1:")
    depends_on("r-glue", type=("build", "run"), when="@1:")
    depends_on("r-knitr", type=("build", "run"), when="@:0.1.9")
    depends_on("r-knitr@1.23:", type=("build", "run"), when="@1:")
    depends_on("r-lifecycle", type=("build", "run"), when="@2.0.2:")
    depends_on("r-rlang", type=("build", "run"), when="@0.2.0:")
    depends_on("r-rlang@0.4.0:", type=("build", "run"), when="@1:")
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@2.0.2:")
    depends_on("r-rmarkdown", type=("build", "run"))
    depends_on("r-rstudioapi", type=("build", "run"), when="@2:")
    depends_on("r-withr", type=("build", "run"), when="@0.2.0:")
    depends_on("r-withr@2.3.0:", type=("build", "run"), when="@1:")
    depends_on("pandoc@1.12.3:")
    depends_on("pandoc@2.0:", when="@2:")

    depends_on("r-whisker", type=("build", "run"), when="@:0")
