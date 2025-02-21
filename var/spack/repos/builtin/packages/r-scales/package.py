# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScales(RPackage):
    """Scale Functions for Visualization.

    Graphical scales map data to aesthetics, and provide methods for
    automatically determining breaks and labels for axes and legends."""

    cran = "scales"

    license("MIT")

    version("1.3.0", sha256="b33e0f6b44259551ce02befd52eac53602509fbfdd903920620c658c50f35888")
    version("1.2.1", sha256="59453e6dbdafee93dfb101e4d86048a62a12898134259d3ef02d65aeec57ed08")
    version("1.2.0", sha256="185d50240e6b3e84d36ec7fbca6aef7a85db7c8c1b0dde51d4af28d363ce02df")
    version("1.1.1", sha256="40b2b66522f1f314a20fd09426011b0cdc9d16b23ee2e765fe1930292dd03705")
    version("1.0.0", sha256="0c1f4a14edd336a404da34a3cc71a6a9d0ca2040ba19360c41a79f36e06ca30c")
    version("0.5.0", sha256="dbfcc0817c4ab8b8777ec7d68ebfe220177c193cfb5bd0e8ba5d365dbfe3e97d")
    version("0.4.1", sha256="642b88fb1fce7bac72a0038ce532b65b8a79dffe826fec25033cf386ab630cd3")
    version("0.4.0", sha256="851ef6136339b361b3f843fb73ea89f9112279b9cc126bdb38acde8d24c1c6a7")

    depends_on("r@2.13:", type=("build", "run"))
    depends_on("r@3.1:", type=("build", "run"), when="@1.0.0:")
    depends_on("r@3.2:", type=("build", "run"), when="@1.1.1:")
    depends_on("r@3.6:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-cli", type=("build", "run"), when="@1.3.0:")
    depends_on("r-farver@2.0.3:", type=("build", "run"), when="@1.1.1:")
    depends_on("r-glue", type=("build", "run"), when="@1.3.0:")
    depends_on("r-labeling", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@1.1.1:")
    depends_on("r-munsell@0.5:", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-viridislite", type=("build", "run"))

    depends_on("r-dichromat", type=("build", "run"), when="@:0.5.0")
    depends_on("r-plyr", type=("build", "run"), when="@:0.5.0")
    depends_on("r-rcpp", type=("build", "run"), when="@:1.0.0")
