# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRsubread(RPackage):
    """Mapping, quantification and variant analysis of sequencing data"""

    bioc = "Rsubread"

    version("2.20.0", commit="423e74535e7ba7bfaa0ab5d325216f9f5e8031a0")
    version("2.18.0", commit="900c3607052ed8c870bc4dbe86f7cfd9c7aea4d7")
    version("2.16.1", commit="b1a6ee9328bdad963cd2c1c1bb9e4cac7b02a0c2")
    version("2.16.0", commit="62b92c9ed3fc2be89ed9f29e3db1809d1e115dbc")
    version("2.14.2", commit="863bd98c6523b888da59335a6acb516d2676d412")

    depends_on("c", type="build")  # generated

    depends_on("r", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("zlib-api", type=("build", "run"))
