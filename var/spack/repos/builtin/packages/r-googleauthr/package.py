# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGoogleauthr(RPackage):
    """Authenticate and Create Google APIs.

    Create R functions that interact with OAuth2 Google APIs
    <https://developers.google.com/apis-explorer/> easily, with auto-refresh
    and Shiny compatibility."""

    cran = "googleAuthR"

    version("2.0.2", sha256="fd55c85b5f78aa52b6e5cabd4143162cb497ab7288c8db3676acf58a0f393996")
    version("2.0.1", sha256="9b19a63bc250151674f20b27389baa95c10cc62dc7c3c0ff12a8d684bdb8a14b")
    version("2.0.0", sha256="ba504baf3bde2e1b3e988bee7602df5765cc6ca542cf0ab76a782c4e60966feb")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-assertthat", type=("build", "run"))
    depends_on("r-assertthat@0.2.0:", type=("build", "run"), when="@2.0.1:")
    depends_on("r-cli", type=("build", "run"))
    depends_on("r-cli@2.0.2:", type=("build", "run"), when="@2.0.1:")
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-gargle@1.2.0:", type=("build", "run"))
    depends_on("r-httr@1.4.0:", type=("build", "run"))
    depends_on("r-jsonlite@1.6:", type=("build", "run"))
    depends_on("r-memoise@1.1.0:", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
