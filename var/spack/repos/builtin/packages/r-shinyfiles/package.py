# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RShinyfiles(RPackage):
    """A Server-Side File System Viewer for Shiny.

    Provides functionality for client-side navigation of the server side file
    system in shiny apps. In case the app is running locally this gives the
    user direct access to the file system without the need to "download" files
    to a temporary location. Both file and folder selection as well as file
    saving is available."""

    cran = "shinyFiles"

    version("0.9.3", sha256="4a72e165ee8a6e8256988f27286a2cfc4d7a42e2a902f4f2a728b1c237c07286")
    version("0.9.2", sha256="8fbe4b8e1478c5e5efdb8fddcbe210fd2275e61d9ff06efa1672f61dd3268ad0")
    version("0.9.1", sha256="05694630ed5ae6ac15307ffcb211c83097fee0f38ca59340a7e68cac62730d39")
    version("0.9.0", sha256="51ad2aad61bcae22fb2c48a79d02bf6f86e36ffc49a3b64e26a76d133a955167")
    version("0.7.3", sha256="710c8a6191aaf336379bc748daff1160d0d2858e2aee0d98e2ad48e7121d5a05")

    depends_on("r-htmltools", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-shiny@1.1.0:", type=("build", "run"))
    depends_on("r-fs@1.2.6:", type=("build", "run"))
    depends_on("r-tibble@1.4.2:", type=("build", "run"))
