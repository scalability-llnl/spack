# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGcrma(RPackage):
    """Background Adjustment Using Sequence Information.

    Background adjustment using sequence information."""

    bioc = "gcrma"

    version("2.72.0", commit="5cfccc7c684283dc3a82830bad75aad254efcb01")
    version("2.70.0", commit="095f38914525d8812524a3cb38db8075382f8121")
    version("2.68.0", commit="c14063ff5490fac8d60530826613d728e68b3d66")
    version("2.66.0", commit="ba134b392def89d36b5639a187e0c25a4353457b")
    version("2.62.0", commit="b91bdf5bf4e875defedb4d4e3e1e75867773287a")
    version("2.56.0", commit="1f37bbfb4d3ed542b1e90704ab0fa8914d5e0224")
    version("2.54.0", commit="9515fdbbc766a2a3b2ec61cf530c57bbded77ccc")
    version("2.52.0", commit="d6e90b05432d2a8b0583d3fed001811ecdf49d7d")
    version("2.50.0", commit="cbba460d131e1073059500b8d7b168a78f963992")
    version("2.48.0", commit="3ea0eb0b5c15ffb24df76620667ae7996ed715b4")

    depends_on("c", type="build")  # generated

    depends_on("r@2.6.0:", type=("build", "run"))
    depends_on("r-affy@1.23.2:", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-affyio@1.13.3:", type=("build", "run"))
    depends_on("r-xvector", type=("build", "run"))
    depends_on("r-biostrings@2.11.32:", type=("build", "run"))
    depends_on("r-biocmanager", type=("build", "run"), when="@2.54.0:")

    depends_on("r-biocinstaller", type=("build", "run"), when="@:2.52.0")
