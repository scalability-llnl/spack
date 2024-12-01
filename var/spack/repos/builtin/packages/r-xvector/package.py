# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXvector(RPackage):
    """Foundation of external vector representation and manipulation in
    Bioconductor.

    Provides memory efficient S4 classes for storing sequences "externally"
    (e.g. behind an R external pointer, or on disk)."""

    bioc = "XVector"

    version("0.40.0", commit="875b4b4469e125737bee42362e7a3c75edd642f1")
    version("0.38.0", commit="8cad08446091dcc7cd759e880c0f3e47228278dd")
    version("0.36.0", commit="ff6f818ff4357eb9bf00654de9e0f508a5285408")
    version("0.34.0", commit="06adb25ac51c707b90fb8e0637fa06df237a863c")
    version("0.30.0", commit="985e963e0b1c3ff004dd0b07ad7c9ff7ed853ec0")
    version("0.24.0", commit="e5109cb2687724b9fddddf296c07a82bae4c551d")
    version("0.22.0", commit="b5e107a5fd719e18374eb836eb498b529afa4473")
    version("0.20.0", commit="a83a7ea01f6a710f0ba7d9fb021cfa795b291cb4")
    version("0.18.0", commit="27acf47282c9880b54d04dff46c1e50f0c87fa6b")
    version("0.16.0", commit="54615888e1a559da4a81de33e934fc0f1c3ad99f")

    depends_on("c", type="build")  # generated

    depends_on("r@2.8.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@0.34.0:")
    depends_on("r-biocgenerics@0.19.2:", type=("build", "run"))
    depends_on("r-biocgenerics@0.37.0:", type=("build", "run"), when="@0.34.0:")
    depends_on("r-s4vectors@0.13.13:", type=("build", "run"))
    depends_on("r-s4vectors@0.15.14:", type=("build", "run"), when="@0.18.0:")
    depends_on("r-s4vectors@0.17.24:", type=("build", "run"), when="@0.20.0:")
    depends_on("r-s4vectors@0.19.15:", type=("build", "run"), when="@0.22.0:")
    depends_on("r-s4vectors@0.21.13:", type=("build", "run"), when="@0.24.0:")
    depends_on("r-s4vectors@0.27.12:", type=("build", "run"), when="@0.30.0:")
    depends_on("r-iranges@2.9.18:", type=("build", "run"))
    depends_on("r-iranges@2.13.16:", type=("build", "run"), when="@0.20.0:")
    depends_on("r-iranges@2.15.12:", type=("build", "run"), when="@0.22.0:")
    depends_on("r-iranges@2.23.9:", type=("build", "run"), when="@0.30.0:")
    depends_on("r-zlibbioc", type=("build", "run"))
    depends_on("zlib-api")
