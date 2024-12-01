# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProxy(RPackage):
    """Distance and Similarity Measures.

    Provides an extensible framework for the efficient calculation of auto- and
    cross-proximities, along with implementations of the most popular ones."""

    cran = "proxy"

    license("GPL-2.0-only")

    version("0.4-27", sha256="249991a4c4d70ad139e93f3a24e17f161ad1ec854951813ea192daf79478563f")
    version("0.4-26", sha256="676bad821343974e0297a0566c4bf0cf0ea890104906a745b87d3b5989c81a4d")
    version("0.4-24", sha256="8cff9bf036475941a7c44ba9bb5e2f6d4777d49ab3daaeb52d23f4b2af6d9c7c")
    version("0.4-23", sha256="9dd4eb0978f40e4fcb55c8a8a26266d32eff9c63ac9dfe70cf1f664ca9c3669d")
    version("0.4-19", sha256="6b27e275018366e6024382704da9a9757c8878535dbcd7d450824b70e2e34d51")

    depends_on("c", type="build")  # generated

    depends_on("r@3.3.2:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@0.4-21:")
