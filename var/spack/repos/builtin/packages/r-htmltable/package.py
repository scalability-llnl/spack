# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHtmltable(RPackage):
    """Advanced Tables for Markdown/HTML.

    Tables with state-of-the-art layout elements such as row spanners, column
    spanners, table spanners, zebra striping, and more. While allowing advanced
    layout, the underlying css-structure is simple in order to maximize
    compatibility with word processors such as 'MS Word' or 'LibreOffice'. The
    package also contains a few text formatting functions that help outputting
    text compatible with HTML/'LaTeX'."""

    cran = "htmlTable"

    version("2.4.3", sha256="3739d01bff313ccd206b63940a8252b037f0521d041c721a4e0d195abd6ef6dd")
    version("2.4.1", sha256="3a7f3e75d886dc398fd1d3cae907b536fff6af3a3d2c18349ef12ec06d310f93")
    version("2.4.0", sha256="4ca2b5616d77cfeee8ae5ca74307b86407d478b12d1ce17ba9c447e233b89a9d")
    version("2.1.0", sha256="4049339b317cbec1c8c7930e2e36cf0fc8b002516092dd270bb794d8db02f0bf")
    version("1.13.1", sha256="689f32b65da6a57ad500e8d9ef3309d346401dca277c6b264a46c8d7c75884d0")
    version("1.11.2", sha256="64a273b1cdf07a7c57b9031315ca665f95d78e70b4320d020f64a139278877d1")
    version("1.9", sha256="5b487a7f33af77db7d987bf61f3ef2ba18bb629fe7b9802409f8b3485c603132")

    depends_on("r@4.1:", type=("build", "run"), when="@2.4.2:")
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-knitr@1.6:", type=("build", "run"))
    depends_on("r-magrittr@1.5:", type=("build", "run"))
    depends_on("r-checkmate", type=("build", "run"))
    depends_on("r-htmlwidgets", type=("build", "run"))
    depends_on("r-htmltools", type=("build", "run"), when="@1.11.0:")
    depends_on("r-rstudioapi@0.6:", type=("build", "run"), when="@1.11.0:")
