# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDebugme(RPackage):
    """Debug R Packages.

    Specify debug messages as special string constants, and control debugging
    of packages via environment variables."""

    cran = "debugme"

    license("MIT")

    version("1.2.0", sha256="b22605ad3b20d460308d8c9c18116e56c4d6ff10577608eaf58802998171f099")
    version("1.1.0", sha256="4dae0e2450d6689a6eab560e36f8a7c63853abbab64994028220b8fd4b793ab1")

    depends_on("r@3.6:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-crayon", type=("build", "run"))
