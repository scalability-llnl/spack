# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProtgenerics(RPackage):
    """S4 generic functions for Bioconductor proteomics infrastructure.

    S4 generic functions needed by Bioconductor proteomics packages."""

    bioc = "ProtGenerics"

    version("1.32.0", commit="30c6458568c43fc7d769b0aef855d6e90b314eaa")
    version("1.30.0", commit="fcd566bf04034cf52db3338b5d6de7447443cf77")
    version("1.28.0", commit="cfcd0a9ebd642515764ba70c5c4e9c2a0f2f07ac")
    version("1.26.0", commit="2033289ab928034b86c321e56c37e502e557c7a1")
    version("1.22.0", commit="2bb3011fb0d79536e1c50251084a7057004449c6")
    version("1.16.0", commit="960a5fdc586898513b5ae9c48fffba5c5d703723")
    version("1.14.0", commit="c85940b70a16ad69275c4facb3ef673d20a1c998")
    version("1.12.0", commit="e84382a4b1730409f572fb681b5070017d00d30d")
    version("1.10.0", commit="9ae2c3710b77381571900f0f25c6c8fda65795ac")
    version("1.8.0", commit="b2b3bb0938e20f58fca905f6870de7dbc9dfd7a3")
