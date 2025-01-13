# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHaven(RPackage):
    """Import and Export 'SPSS', 'Stata' and 'SAS' Files.

    Import foreign statistical formats into R via the embedded 'ReadStat' C
    library, <https://github.com/WizardMac/ReadStat>."""

    cran = "haven"

    license("MIT")

    version("2.5.4", sha256="9e1531bb37aa474abd91db5e0ed9e3a355c03faa65f4e653b3ea68b7c61ea835")
    version("2.5.3", sha256="9a5999afad09f0cf80515241b2ff19a0c480658c4bd3810638ad52762e04b7e3")
    version("2.5.2", sha256="2131fb0377ae1beffae54bf4beb8b3a876e9b6b9841a5acc39a2a2615023561d")
    version("2.5.1", sha256="9f40462097a0b1cf3831bca493851fe4a6b3570d957a775ca81940f241c50a70")
    version("2.5.0", sha256="b580311bc1b28efc6b123e29a331282b9f7eb552c485f4e5cacab39fe534aff4")
    version("2.4.3", sha256="95b70f47e77792bed4312441787299d2e3e27d79a176f0638a37e5301b93295f")
    version("2.3.1", sha256="6eee9f3297aab4cae2e4a4181ea65af933eacee2a2fb40af5b2ecf06f1bb9e0d")
    version("2.1.1", sha256="90bcb4e7f24960e7aa3e15c06b95cd897f08de149cec43fd8ba110b14526068a")
    version("2.1.0", sha256="c0a1cf1b039549fb3ad833f9644ed3f142790236ad755d2ee7bd3d8109e3ae74")
    version("1.1.0", sha256="089fb4d0955f320abc48d0a3031799f96f3a20b82492474743903fdf12001d19")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.2:", type=("build", "run"), when="@2.1.1:")
    depends_on("r@3.4:", type=("build", "run"), when="@2.5.0:")
    depends_on("r@3.6:", type=("build", "run"), when="@2.5.4:")
    depends_on("r-cli@3.0.0:", type=("build", "run"), when="@2.5.0:")
    depends_on("r-forcats@0.2.0:", type=("build", "run"))
    depends_on("r-hms", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@2.5.0:")
    depends_on("r-readr@0.1.0:", type=("build", "run"))
    depends_on("r-rlang@0.4.0:", type=("build", "run"), when="@2.3.1:")
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-tidyselect", type=("build", "run"), when="@2.3.1:")
    depends_on("r-vctrs@0.3.0:", type=("build", "run"), when="@2.3.1:")
    depends_on("r-cpp11", type=("build", "run"), when="@2.4:")
    depends_on("gmake", type="build")
    depends_on("zlib-api", when="@2.4:")

    depends_on("r-rcpp@0.11.4:", type=("build", "run"), when="@:2.3")
