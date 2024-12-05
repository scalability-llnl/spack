# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RManipulatewidget(RPackage):
    """Add Even More Interactivity to Interactive Charts.

    Like package 'manipulate' does for static graphics, this package helps to
    easily add controls like sliders, pickers, checkboxes, etc. that can be
    used to modify the input data or the parameters of an interactive chart
    created with package 'htmlwidgets'."""

    cran = "manipulateWidget"

    version("0.11.1", sha256="5b73728d7d6dcc32f32d861375074cd65112c03a01e4ee4fa94e21b063fdefb6")
    version("0.10.1", sha256="9d621192121f6b516bc7f1a18305995bfb7838c6683ac701422afc03a50e27ee")
    version("0.10.0", sha256="3d61a3d0cedf5c8a850a3e62ed6af38c600dc3f25b44c4ff07a5093bf9ca4ffd")
    version("0.9.0", sha256="5bf4bdb702263b0e156f40f3354922a06db7db544e497addcd6c98d9860bf3a3")
    version("0.8.0", sha256="e7e6351b1fb8f39b9895e2536fa7c149cbc5d63d7022f67c1b25232cf0706ca7")
    version("0.7.0", sha256="160ce5c68658301e00051c60ac5693701c5bc97b7344bacde0f56be4955231f6")
    version("0.6.0", sha256="90aa1b30647d7034166b8d6c6185503b6855c70253e36a41742a84faa77ce0db")
    version("0.5.1", sha256="5a672c2bd8ba16ec8212cd9fb620072b243e6d18c02dd3ec70bd8c2a1ff1c9c4")
    version("0.5.0", sha256="2599e25f78bb0d748705160e1dfe62a673f5bb388ac5f415f3d649d2511737c8")
    version("0.4.0", sha256="65cc7d28c2b2efc81fda35da019ac6e6058580cf0fdf5e31458cc96386c0c599")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-shiny@1.0.3:", type=("build", "run"))
    depends_on("r-miniui", type=("build", "run"))
    depends_on("r-htmltools", type=("build", "run"))
    depends_on("r-htmlwidgets", type=("build", "run"))
    depends_on("r-knitr", type=("build", "run"))
    depends_on("r-base64enc", type=("build", "run"))
    depends_on("r-codetools", type=("build", "run"))
    depends_on("r-webshot", type=("build", "run"))
    depends_on("r-shinyjs", type=("build", "run"), when="@0.11.1:")
