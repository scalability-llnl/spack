# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPurrr(RPackage):
    """Functional Programming Tools.

    A complete and consistent functional programming toolkit for R."""

    cran = "purrr"

    license("MIT")

    version("1.0.2", sha256="2c1bc6bb88433dff0892b41136f2f5c23573b335ff35a4775c72aa57b48bbb63")
    version("1.0.1", sha256="0a7911be3539355a4c40d136f2602befcaaad5a3f7222078500bfb969a6f2ba2")
    version("0.3.5", sha256="a2386cd7e78a043cb9c14703023fff15ab1c879bf648816879d2c0c4a554fcef")
    version("0.3.4", sha256="23ebc93bc9aed9e7575e8eb9683ff4acc0270ef7d6436cc2ef4236a9734840b2")
    version("0.3.2", sha256="27c74dd9e4f6f14bf442473df22bcafc068822f7f138f0870326532f143a9a31")
    version("0.3.1", sha256="c2a3c9901192efd8a04976676f84885a005db88deb1432e4750900c7b3b7883b")
    version("0.2.4", sha256="ed8d0f69d29b95c2289ae52be08a0e65f8171abb6d2587de7b57328bf3b2eb71")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.2:", type=("build", "run"), when="@0.3.3:")
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.0.1:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.0.2:")
    depends_on("r-vctrs@0.5.0:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-vctrs@0.6.3:", type=("build", "run"), when="@1.0.2:")
    depends_on("r-lifecycle@1.0.3:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-cli@3.4.0:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-cli@3.6.1:", type=("build", "run"), when="@1.0.2:")
    depends_on("r-magrittr@1.5:", type=("build", "run"))
    depends_on("r-magrittr@1.5.0:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-rlang@0.3.1:", type=("build", "run"))
    depends_on("r-rlang@0.4.10:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-rlang@1.1.1:", type=("build", "run"), when="@1.0.2:")

    depends_on("r-tibble", type=("build", "run"), when="@:0.2.9")
