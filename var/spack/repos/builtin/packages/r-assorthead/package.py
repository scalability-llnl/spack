# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssorthead(RPackage):
    """Assorted header-only C++ libraries for Bioconductor."""

    bioc = "assorthead"

    version("1.1.9", commit="b9de4f460dcac95360ae124cfe6c551863213dc6")
