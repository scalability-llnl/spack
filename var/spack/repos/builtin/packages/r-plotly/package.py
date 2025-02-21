# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPlotly(RPackage):
    """Create Interactive Web Graphics via 'plotly.js'.

    Create interactive web graphics from 'ggplot2' graphs and/or a custom
    interface to the (MIT-licensed) JavaScript library 'plotly.js' inspired by
    the grammar of graphics."""

    cran = "plotly"

    license("MIT")

    version("4.10.4", sha256="cfa995b7ed55d31a196707a3ae6ea352dd907cef3058a3bf1956fde39366d867")
    version("4.10.1", sha256="ac0921a1cba24e17a0f3a0a28b7a40ac930e17fe5caa9c3973c9a8d1e20c367a")
    version("4.10.0", sha256="bd995c654dbc8c09a84adaba8def99766919e3894caf18b551bb26b2f591389a")
    version("4.9.3", sha256="d44d1a16d96de28bc2d36f1c897384215eeec44d109546c6e9c2707db0880120")
    version("4.9.0", sha256="f761148338231f210fd7fe2f8325ffe9cfdaaaeddd7b933b65c44ebb4f85e2cf")
    version("4.8.0", sha256="78f90282c831bbbb675ed4811fb506a98dd05e37251fabd42ebc263c80bae8a6")
    version("4.7.1", sha256="7cd4b040f9bfd9356a8a2aba59ccf318cae6b5d94ded7463e2e823c10fa74972")
    version("4.7.0", sha256="daf2af53b4dc9413805bb62d668d1a3defbb7f755e3440e657195cdf18d318fc")
    version("4.6.0", sha256="c0de45b2aff4122dc8aa9dbfe1cd88fa0a50e9415f397b5fe85cbacc0156d613")
    version("4.5.6", sha256="1d3a4a4ff613d394a9670664fbaf51ddf7fc534278443b4fd99dd1eecf49dc27")
    version("4.5.2", sha256="81ff375d4da69aeabe96e8edf2479c21f0ca97fb99b421af035a260f31d05023")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.0.0:", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-httr", type=("build", "run"))
    depends_on("r-httr@1.3.0:", type=("build", "run"), when="@4.9.3:")
    depends_on("r-jsonlite@1.6:", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-viridislite", type=("build", "run"))
    depends_on("r-base64enc", type=("build", "run"))
    depends_on("r-htmltools@0.3.6:", type=("build", "run"))
    depends_on("r-htmlwidgets@1.3:", type=("build", "run"))
    depends_on("r-htmlwidgets@1.5.2.9001:", type=("build", "run"), when="@4.9.3:")
    depends_on("r-tidyr", type=("build", "run"))
    depends_on("r-tidyr@1.0.0:", type=("build", "run"), when="@4.10.0:")
    depends_on("r-rcolorbrewer", type=("build", "run"), when="@4.6.0:")
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-vctrs", type=("build", "run"), when="@4.9.3:")
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-lazyeval@0.2.0:", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@4.8.0:")
    depends_on("r-rlang@0.4.10:", type=("build", "run"), when="@4.10.0:")
    depends_on("r-crosstalk", type=("build", "run"), when="@4.6.0:")
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"), when="@4.7.0:")
    depends_on("r-promises", type=("build", "run"), when="@4.8.0:")

    depends_on("r-hexbin", type=("build", "run"), when="@:4.9.0")
