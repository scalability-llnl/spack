# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTigris(RPackage):
    """Load Census TIGER/Line Shapefiles.

    Download TIGER/Line shapefiles from the United States Census Bureau and
    load into R as 'SpatialDataFrame' or 'sf' objects."""

    cran = "tigris"

    license("MIT")

    version("2.1", sha256="796bed6ce003323815d606886472bf21c101656fca8a593daa3b69cb3bd6fd97")
    version("2.0.1", sha256="d87c6b0c11ffb967699d345c6bfcfa82581a0753e1130bf0c927b2960b074d8c")
    version("1.6.1", sha256="927e8da3f7120bcc10f0b4ded95687512693e069f082eea7aea6302a2f1b2db2")
    version("1.6", sha256="fa14fbbaf44f5ade1cc92e6e4e4ed2e775bc7c106310711d16b0135a948a1661")
    version("1.5", sha256="5ef71ca83817ad6b97ee86d1e560e8e86ee21bdcb1807ce40c945b3213c04472")
    version("1.0", sha256="97c76568c7cf0615abcbf923a0b4387f6b8c1915b9eb42d0c34cb0f707654403")
    version("0.8.2", sha256="ed8d6ab25332c2cc800858d58324bd8264772d8a916a3f0a8d489250a7e7140e")
    version("0.5.3", sha256="6ecf76f82216798465cd9704acb432caea47469ffc4953f1aaefa4d642a28445")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.3.0:", type=("build", "run"), when="@0.6.1:")
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-rappdirs", type=("build", "run"))
    depends_on("r-httr", type=("build", "run"))
    depends_on("r-uuid", type=("build", "run"))
    depends_on("r-sf", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))

    depends_on("r-rgeos", type=("build", "run"), when="@:0.5.3")
    depends_on("r-maptools", type=("build", "run"), when="@:1.6.1")
    depends_on("r-rgdal", type=("build", "run"), when="@:1.6.1")
    depends_on("r-sp", type=("build", "run"), when="@:1.6.1")
