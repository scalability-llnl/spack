# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RFormatr(RPackage):
    """Format R Code Automatically.

    Provides a function tidy_source() to format R source code. Spaces and
    indent will be added to the code automatically, and comments will be
    preserved under certain conditions, so that R code will be more
    human-readable and tidy. There is also a Shiny app as a user interface in
    this package."""

    cran = "formatR"

    version("1.14", sha256="4ebaab2c3f8527871655246b62abd060bc75dae1cec7f962ca4752b8080f474c")
    version("1.12", sha256="8b52efbf43cbef25d837bb99a793a590c0958b753052c032b52304724e808c8b")
    version("1.11", sha256="bd81662d09cf363652761e63ba5969c71be4dd5ae6fc9098f440d6729254a30c")
    version("1.7", sha256="a366621b3ff5f8e86a499b6f87858ad47eefdace138341b1377ecc307a5e5ddb")
    version("1.6", sha256="f5c98f0c3506ca51599671a2cdbc17738d0f326e8e3bb18b7a38e9f172122229")
    version("1.5", sha256="874c197ae3720ec11b44984a055655b99a698e1912104eb9034c11fdf6104da7")
    version("1.4", sha256="6ec47a7b1f18efb5fd7559b81427363b66415d81cded9d5e7e2907e900b67ebb")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.2.3:", type=("build", "run"), when="@1.11:")
