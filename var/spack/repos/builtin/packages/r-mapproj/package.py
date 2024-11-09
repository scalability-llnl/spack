# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMapproj(RPackage):
    """Map Projections.

    Converts latitude/longitude into projected coordinates."""

    cran = "mapproj"

    license("LPL-1.02")

    version("1.2.11", sha256="db2d201cc939de26717566066bf44225a967ccde6fc34731af845f03c086347d")
    version("1.2.9", sha256="da28fab490072e0b2ff5e124092d6b3146e4c01b2386e23a2ea4b0e9fc72df82")
    version("1.2.8", sha256="865f108f1ee54cda38571b86cd46063a903824d9b4eabfdf75218023d08a7781")
    version("1.2.7", sha256="f0081281b08bf3cc7052c4f1360d6d3c20d9063be57754448ad9b48ab0d34c5b")
    version("1.2.6", sha256="62a5aa97837ae95ef9f973d95fe45fe43dbbf482dfa922e9df60f3c510e7efe5")
    version("1.2-5", sha256="f3026a3a69a550c923b44c18b1ccc60d98e52670a438250d13f3c74cf2195f66")
    version("1.2-4", sha256="cf8a1535f57e7cca0a71b3a551e77ad3e7a78f61a94bb19effd3de19dbe7dceb")

    depends_on("c", type="build")  # generated

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-maps@2.3-0:", type=("build", "run"))
