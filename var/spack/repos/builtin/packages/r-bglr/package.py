# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBglr(RPackage):
    """Bayesian Generalized Linear Regression."""

    cran = "BGLR"

    license("GPL-3.0-only")

    version("1.1.2", sha256="39476f3739bd86905a379e2d5de86ef1f8b0e10c311e350d95ce7aadb7b28224")
    version("1.1.0", sha256="97c5bb8a461eb408e907693811b2d917efc993000da06591a83a3f5529451ea7")
    version("1.0.9", sha256="440a96f9f502e0d6ecc8c00720d1ccdbab5ee8223e1def6c930edaa9a9de9099")
    version("1.0.8", sha256="5e969590d80b2f272c02a43b487ab1ffa13af386e0342993e6ac484fc82c9b95")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-truncnorm", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"), when="@1.0.9:")
