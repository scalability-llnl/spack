# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRsconnect(RPackage):
    """Deployment Interface for R Markdown Documents and Shiny Applications.

    Programmatic deployment interface for 'RPubs', 'shinyapps.io', and 'RStudio
    Connect'. Supported content types include R Markdown documents, Shiny
    applications, Plumber APIs, plots, and static web content."""

    cran = "rsconnect"

    license("GPL-2.0-only")

    version("1.3.1", sha256="47de8a832da493e2a1b3243fb42459a53eb193f75a1143348b7d8c7478cb5557")
    version("0.8.29", sha256="852899d2aaf90bcedf4d191a9e00c770e8ee4233235169fc97e6aa636de01c43")
    version("0.8.28", sha256="25b9a947772ada9593da5c48297b7a7dd0e11aa73fbb9a282631c75ec49616e0")
    version("0.8.27", sha256="0a44d5605fc7cd6855ea0235d662e4a323a24a2c214cc4f1696afbca3a8f169c")
    version("0.8.26", sha256="faafabbed803743799b345051f221aef2b4497b421fc98092ca41c05ef6b5fed")
    version("0.8.25", sha256="3c055277f745f2ca37a73e2f425249307cea4dc95ecc59fbe05ee8b6cf26d9cf")
    version("0.8.17", sha256="64767a4d626395b7871375956a9f0455c3d64ff6e779633b0e554921d85da231")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-curl", type=("build", "run"))
    depends_on("r-cli", type=("build", "run"), when="@1.0.0:")
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@1.0.0:")
    depends_on("r-openssl", type=("build", "run"))
    depends_on("r-openssl@2.0.0:", type=("build", "run"), when="@0.8.26:")
    depends_on("r-packrat@0.6:", type=("build", "run"), when="@0.8.18:")
    depends_on("r-packrat@0.5:", type=("build", "run"))
    depends_on("r-packrat@0.6:", type=("build", "run"), when="@0.8.26:")
    depends_on("r-pki", type=("build", "run"), when="@1.2.2:")
    depends_on("r-renv@1.0.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-rstudioapi@0.5:", type=("build", "run"))
    depends_on("r-yaml@2.1.5:", type=("build", "run"))
