# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRUtils(RPackage):
    """Various Programming Utilities.

    Utility functions useful when programming and developing R packages."""

    cran = "R.utils"

    version("2.12.3", sha256="74d6e77a95a23381a490fea54be01b653d4b938a2dc75e749a694ab48302c40c")
    version("2.12.2", sha256="fe3cf1aa8641540634e96990294d0202d4d94ec79ce73aaf78e4eda30fcb8836")
    version("2.12.1", sha256="3eb82903bee99f9684cd9dbd4f92d682fdb82feb7ff32a70aa54550e9e09ad62")
    version("2.12.0", sha256="74de455220ea1e658ac503f5763a6be687d982eb61187779f4019a16db856503")
    version("2.11.0", sha256="622860f995f78be3a6e439f29d945874c5cb0866f6a73a9b43ac1d4d7f23fed8")
    version("2.10.1", sha256="957a4f51998c79403a50f6a46266e6553bbf08757b26bf80603a423bceb45abf")
    version("2.9.0", sha256="b2aacc5a55d3ea86c41ac576d2583e446af145f4cb1103ad7b6f95b09ab09ff0")
    version("2.5.0", sha256="1ae1a0f0c6a4972bb2369a2dbccd29ade87d747255ff9cb5a0bd784a5be1039f")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r-r-oo@1.22.0:", type=("build", "run"))
    depends_on("r-r-oo@1.23.0:", type=("build", "run"), when="@2.10.1:")
    depends_on("r-r-oo@1.24.0:", type=("build", "run"), when="@2.11.0:")
    depends_on("r-r-methodss3@1.7.1:", type=("build", "run"))
    depends_on("r-r-methodss3@1.8.0:", type=("build", "run"), when="@2.10.1:")
    depends_on("r-r-methodss3@1.8.1:", type=("build", "run"), when="@2.11.0:")
