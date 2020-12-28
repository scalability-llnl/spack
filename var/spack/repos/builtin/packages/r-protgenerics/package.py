# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProtgenerics(RPackage):
    """S4 generic functions for Bioconductor proteomics infrastructure.

       S4 generic functions needed by Bioconductor proteomics packages."""

    homepage = "https://bioconductor.org/packages/ProtGenerics"
    git      = "https://git.bioconductor.org/packages/ProtGenerics.git"

    version('1.16.0', commit='960a5fdc586898513b5ae9c48fffba5c5d703723')
    version('1.14.0', commit='c85940b70a16ad69275c4facb3ef673d20a1c998')
    version('1.12.0', commit='e84382a4b1730409f572fb681b5070017d00d30d')
    version('1.10.0', commit='9ae2c3710b77381571900f0f25c6c8fda65795ac')
    version('1.8.0', commit='b2b3bb0938e20f58fca905f6870de7dbc9dfd7a3')
