# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTseries(RPackage):
    """Time series analysis and computational finance."""

    cran = "tseries"

    license("GPL-2.0-only")

    version("0.10-57", sha256="18754bb7642728916e30e67cb75462a296699b9b1f2ef1fb9803199f00f89bee")
    version("0.10-53", sha256="ec388ee6d022752bbebbecbf22d793d31f3734982e3f2e3ffd8dde14bffcca56")
    version("0.10-52", sha256="9399c8dbedb3b44b8b3b854f6e8867e0a14f3727a7aa66ec9c6eff069ead8f45")
    version("0.10-51", sha256="a55f20704883710ab58ea479e20cf0f263c50d54282f693793cda4af664c207f")
    version("0.10-49", sha256="45bf26d8f41f12a72954bbe5fb6f4da6cc4ef29ee075c49fe7cc8456926c14ba")
    version("0.10-48", sha256="53bd22708c936205c5f839a10f2e302524d2cc54dc309e7d885ebd081ccb4471")
    version("0.10-47", sha256="202377df56806fe611c2e12c4d9732c71b71220726e2defa7e568d2b5b62fb7b")
    version("0.10-46", sha256="12940afd1d466401160e46f993ed4baf28a42cef98d3757b66ee15e916e07222")
    version("0.10-42", sha256="827f79858715c700e8cabd2c27853ba88ad0e05eb043bc94e126b155a75546c4")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@0.10-57:")
    depends_on("r-jsonlite", type=("build", "run"), when="@0.10-54:")
    depends_on("r-quadprog", type=("build", "run"))
    depends_on("r-zoo", type=("build", "run"))
    depends_on("r-quantmod@0.4-9:", type=("build", "run"))
