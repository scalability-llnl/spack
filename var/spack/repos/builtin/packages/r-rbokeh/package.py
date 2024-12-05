# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRbokeh(RPackage):
    """R Interface for Bokeh.

    A native R plotting library that provides a flexible declarative interface
    for creating interactive web-based graphics, backed by the Bokeh
    visualization library <https://bokeh.pydata.org/>."""

    cran = "rbokeh"

    license("BSD-3-Clause")

    version("0.5.2", sha256="d8c47dbd978efce04e5676a3a91d511517a9bb8fe1859c404bfc9ee0f0bf4ec0")
    version("0.5.1", sha256="48eba3b238cea2b9aa408d8a48c663564292e76f2ab3f603bc671315a4a75a88")
    version("0.5.0", sha256="499c3224a7dcaeb4bb60fd645b3ef528a20e59437747a073713941b80cbcebd2")

    depends_on("r+X", type=("build", "run"))
    depends_on("r-htmlwidgets@0.5:", type=("build", "run"))
    depends_on("r-maps", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-hexbin", type=("build", "run"))
    depends_on("r-lazyeval", type=("build", "run"))
    depends_on("r-pryr", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-gistr", type=("build", "run"))

    depends_on("r-ggplot2", type=("build", "run"), when="@:0.5.1")
