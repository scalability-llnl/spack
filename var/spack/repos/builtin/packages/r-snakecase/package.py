# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSnakecase(RPackage):
    """Convert Strings into any Case.

    A consistent, flexible and easy to use tool to parse and convert strings
    into cases like snake or camel among others."""

    cran = "snakecase"

    license("GPL-3.0-only")

    version("0.11.1", sha256="2a5f9791337ca42e392f23fb873eb44f74810583e9aa7c62fda2f28f9e750821")
    version("0.11.0", sha256="998420a58391ac85785e60bcdf6fd6927c82758ad2859a9a73a0e57299e8c1cf")

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-stringi", type=("build", "run"))
