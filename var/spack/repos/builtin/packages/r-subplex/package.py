# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSubplex(RPackage):
    """Unconstrained Optimization using the Subplex Algorithm.

    The subplex algorithm for unconstrained optimization, developed by Tom
    Rowan <https://www.netlib.org/opt/subplex.tgz>."""

    cran = "subplex"

    license("GPL-3.0-only")

    version("1.9", sha256="07a9ea8cba46a6eec037f8c6e87279c122479ccc560a96bd3086d653f95d69b7")
    version("1.8", sha256="3bc31d8990380c9f790c9c7d84cb2e39f4945eff934eddfa1196d597465be5a5")
    version("1.7", sha256="d5ecf4a484936d71cb294f08c3968ef5a8dcbdc861bfc0e97e3b1ab99afff887")
    version("1.6", sha256="0d05da1622fffcd20a01cc929fc6c2b7df40a8246e7018f7f1f3c175b774cbf9")
    version("1.5-4", sha256="ff94cf6b1560f78c31712c05bc2bc1b703339e09c7fc777ee94abf15fa7a8b81")
    version("1.5-2", sha256="6f8c3ccadf1ccd7f11f3eae28cec16eed3695f14e351b864d807dbaba6cd3ded")
    version("1.4-1", sha256="94b7b961aaa229a6f025151191ed50272af1394be69f1c41146b9e8c786caec6")

    depends_on("r@2.5.1:", type=("build", "run"))
    depends_on("r@4.1.0:", type=("build", "run"), when="@1.9:")
