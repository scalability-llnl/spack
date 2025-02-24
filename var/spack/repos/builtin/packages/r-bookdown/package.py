# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBookdown(RPackage):
    """Authoring Books and Technical Documents with R Markdown.

    Output formats and utilities for authoring books and technical documents
    with R Markdown."""

    cran = "bookdown"

    license("GPL-3.0-only")

    version("0.40", sha256="58df4a044704b6c42a397f4e430a7fc8f6171bad1447872119aceafd158eac39")
    version("0.33", sha256="2288e1d0c383e6ab49202a18db6cc1a04c3adc1b25da646cc46167bc6c2892c3")
    version("0.29", sha256="5b4e3dc44a5c6574e3d9e19ebe7897d3ddcf6eaffe8214e1d272b545929ff723")
    version("0.26", sha256="c6207288cb72ea7c555cbad449c61278e94b742cac1f610879fb3f2d60b2b185")
    version("0.24", sha256="8bead2a20542d05f643fe77a949689a17b0ae9ff23efbb918ddab47597db1be3")
    version("0.21", sha256="47c0fa7a65da83753c2f445e0e972913f9203460f1daae3ab255d0d4b30eba76")
    version("0.12", sha256="38eb4c5b877ccd85b16cfe74a48c3bc53de2f276da98e5515f37e7a06e065bb0")
    version("0.5", sha256="b7331fd56f64bd2bddc34e2a188fc491f9ff5308f44f7e3151721247f21ca67e")

    depends_on("r@3.5.0:", type=("build", "run"), when="@0.33:")

    depends_on("r+X", type=("build", "run"))
    depends_on("r-htmltools@0.3.6:", type=("build", "run"))
    depends_on("r-knitr@1.22:", type=("build", "run"))
    depends_on("r-knitr@1.31:", type=("build", "run"), when="@0.24:")
    depends_on("r-knitr@1.38:", type=("build", "run"), when="@0.29:")
    depends_on("r-rmarkdown@1.12:", type=("build", "run"))
    depends_on("r-rmarkdown@2.4:", type=("build", "run"), when="@0.21:")
    depends_on("r-rmarkdown@2.9:", type=("build", "run"), when="@0.24:")
    depends_on("r-rmarkdown@2.13:", type=("build", "run"), when="@0.26:")
    depends_on("r-rmarkdown@2.14:", type=("build", "run"), when="@0.29:")
    depends_on("r-jquerylib", type=("build", "run"), when="@0.24:")
    depends_on("r-xfun@0.6:", type=("build", "run"))
    depends_on("r-xfun@0.13:", type=("build", "run"), when="@0.21:")
    depends_on("r-xfun@0.22:", type=("build", "run"), when="@0.24:")
    depends_on("r-xfun@0.29:", type=("build", "run"), when="@0.26:")
    depends_on("r-xfun@0.39:", type=("build", "run"), when="@0.34:")
    depends_on("r-tinytex@0.12:", type=("build", "run"), when="@0.12:")
    depends_on("r-yaml@2.1.14:", type=("build", "run"))
    depends_on("r-yaml@2.1.19:", type=("build", "run"), when="@0.21:")
    depends_on("pandoc@1.17.2:")
