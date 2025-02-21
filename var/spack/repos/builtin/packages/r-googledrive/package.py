# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGoogledrive(RPackage):
    """An Interface to Google Drive.

    Manage Google Drive files from R."""

    cran = "googledrive"

    license("MIT")

    version("2.1.1", sha256="0b8b4f74ba3630b0347249a32a80bc5fc2e8b63ad2952702f30162bd2d38fb82")
    version("2.1.0", sha256="0d70353bbf1bebc96d3987ebd9cbb2b0902e6ddc4cdccece3d07c2bb688c4b74")
    version("2.0.0", sha256="605c469a6a086ef4b049909c2e20a35411c165ce7ce4f62d68fd39ffed8c5a26")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@2.1.0:")
    depends_on("r@3.6:", type=("build", "run"), when="@2.1.1:")
    depends_on("r-cli@3.0.0:", type=("build", "run"))
    depends_on("r-gargle@1.2.0:", type=("build", "run"))
    depends_on("r-gargle@1.3.0:", type=("build", "run"), when="@2.1.0:")
    depends_on("r-gargle@1.5.0:", type=("build", "run"), when="@2.1.1:")
    depends_on("r-glue@1.4.2:", type=("build", "run"))
    depends_on("r-httr", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-pillar", type=("build", "run"))
    depends_on("r-pillar@1.9.0:", type=("build", "run"), when="@2.1.1:")
    depends_on("r-purrr@0.2.3:", type=("build", "run"))
    depends_on("r-purrr@1.0.1:", type=("build", "run"), when="@2.1.0:")
    depends_on("r-rlang@0.4.9:", type=("build", "run"))
    depends_on("r-rlang@1.0.2:", type=("build", "run"), when="@2.1.0:")
    depends_on("r-tibble@2.0.0:", type=("build", "run"))
    depends_on("r-uuid", type=("build", "run"))
    depends_on("r-vctrs@0.3.0:", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"))
