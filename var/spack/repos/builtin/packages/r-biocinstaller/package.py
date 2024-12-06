# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocinstaller(RPackage):
    """Install/Update Bioconductor, CRAN, and github Packages.

    This package is used to install and update Bioconductor, CRAN, and
    (some) github packages."""

    bioc = "BiocInstaller"

    version("1.33.1", commit="6193f31c18e7e64d91e0e15ed0ba6924eda1416f")
    version("1.32.1", commit="4c2a39e1cae470af3a5cf1491715f272b70f4bb4")
    version("1.30.0", commit="27bcb7a378cb5d8b5d23b7b840340463f7e090bc")
    version("1.28.0", commit="7261763529a0a1f730cde8a1bbdbf454c3e25603")
    version("1.26.1", commit="9049b82a77aefa98e3f8e4dd7068317505d70e98")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.30.0:")
