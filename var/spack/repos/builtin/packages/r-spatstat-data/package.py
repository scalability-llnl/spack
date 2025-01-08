# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstatData(RPackage):
    """Datasets for 'spatstat' Family.

    Contains all the datasets for the 'spatstat' family of packages."""

    cran = "spatstat.data"

    version("3.1-2", sha256="9b9b416303b8040f723400f3dc454cda75cff1d958660767e7b824503b490b77")
    version("3.0-1", sha256="8eeb4b1de356e9cef42f58b5e0fc7ced2a476a1306e09395ba97253b22dd5300")
    version("3.0-0", sha256="cff9058a88489020a4a05b9576cd452f37fa9b42084873c474d06931f5187057")
    version("2.2-0", sha256="d3943bb4f6509d60bf68e79ce4533c5ec5261f411da6b0ef5238c124fc37c3e5")
    version("2.1-2", sha256="bbd118a8e6cd2c41abc764b9f2e798514070862f11e3f2080c27f72268271ae5")
    version("1.7-0", sha256="bbc192d43f2b37b308566694cb48ecdbbc4f20ef44b6fc7636564a717a03c12f")
    version("1.4-3", sha256="8955b6ac40cc7d0d89e02334bb46f4c223ff0755e5818f132fee753e77918ea2")
    version("1.4-0", sha256="121e5bb92beb7ccac920f921e760f429fd71bcfe11cb9b07a7e7326c7a72ec8c")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.7-0:")
    depends_on("r-spatstat-utils", type=("build", "run"))
    depends_on("r-spatstat-utils@2.1-0:", type=("build", "run"), when="@2.1-2:")
    depends_on("r-spatstat-utils@3.0-0:", type=("build", "run"), when="@3.0-0:")
    depends_on("r-spatstat-utils@3.0-2:", type=("build", "run"), when="@3.0-1:")
    depends_on("r-spatstat-utils@3.0-5:", type=("build", "run"), when="@3.1-2:")
    depends_on("r-matrix", type=("build", "run"))
