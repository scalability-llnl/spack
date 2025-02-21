# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCrosstalk(RPackage):
    """Inter-Widget Interactivity for HTML Widgets.

    Provides building blocks for allowing HTML widgets to communicate with each
    other, with Shiny or without (i.e. static .html files). Currently supports
    linked brushing and filtering."""

    cran = "crosstalk"

    license("MIT")

    version("1.2.1", sha256="680cf08416d6d5a1194dd85ee5695c268af9d4d01b201448e1d486c6e06014f1")
    version("1.2.0", sha256="4237baab35cd246a8a98fb9cf4ce53b6ddbc31d00742ded4edea0479613d1ea0")
    version("1.1.0.1", sha256="36a70b10bc11826e314c05f9579fd791b9ac3b3a2cfed4d4ca74ce1ad991300e")
    version("1.0.0", sha256="b31eada24cac26f24c9763d9a8cbe0adfd87b264cf57f8725027fe0c7742ca51")

    depends_on("r-htmltools@0.3.5:", type=("build", "run"))
    depends_on("r-htmltools@0.3.6:", type=("build", "run"), when="@1.1.0.1:")
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-lazyeval", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))

    depends_on("r-ggplot2", type=("build", "run"), when="@:1.0.0")
    depends_on("r-shiny@0.11:", type=("build", "run"), when="@:1.0.0")
