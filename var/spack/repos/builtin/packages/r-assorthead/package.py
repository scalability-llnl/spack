# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssorthead(RPackage):
    """Assorted header-only C++ libraries for Bioconductor."""

    bioc = "assorthead"

    version("1.0.1", commit="4aa44624adb6981c75db9f5e200114784f343e32")
