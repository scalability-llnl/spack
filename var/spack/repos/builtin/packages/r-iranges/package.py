# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIranges(RPackage):
    """Foundation of integer range manipulation in Bioconductor.

    Provides efficient low-level and highly reusable S4 classes for storing,
    manipulating and aggregating over annotated ranges of integers.
    Implements an algebra of range operations, including efficient
    algorithms for finding overlaps and nearest neighbors. Defines efficient
    list-like classes for storing, transforming and aggregating large
    grouped data, i.e., collections of atomic vectors and DataFrames."""

    bioc = "IRanges"

    version("2.34.0", commit="dcddf934384e05dccffb2a8a808147c963ff0c3e")
    version("2.32.0", commit="2b5c9fc706c8cdc96f0c46508087863df1502f81")
    version("2.30.1", commit="ead506a14d6cc89ac2f14b55a4b04496755e4e50")
    version("2.30.0", commit="9b5f3ca12812fb76c23b1550aa3a794384384d9b")
    version("2.28.0", commit="d85ee908a379e12d1e32599e999c71ab37c25e57")
    version("2.24.1", commit="6c61fddf4c5830f69a0f7f108888c67cd0a12b19")
    version("2.22.2", commit="8c5e99131c419224f92921b9a13255b705a293ad")
    version("2.18.3", commit="c98a7ba074e72f2e5ec98252dffe9d3392711972")
    version("2.16.0", commit="26834c6868d7c279dd8ac1bb9daa16e6fef273c2")
    version("2.14.12", commit="00af02756c14771a23df9efcf379409ab6eb3041")
    version("2.12.0", commit="1b1748655a8529ba87ad0f223f035ef0c08e7fcd")
    version("2.10.5", commit="b00d1d5025e3c480d17c13100f0da5a0132b1614")

    depends_on("c", type="build")  # generated

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@2.24.1:")
    depends_on("r-biocgenerics@0.21.1:", type=("build", "run"))
    depends_on("r-biocgenerics@0.23.3:", type=("build", "run"), when="@2.12.0:")
    depends_on("r-biocgenerics@0.25.3:", type=("build", "run"), when="@2.14.12:")
    depends_on("r-biocgenerics@0.36.0:", type=("build", "run"), when="@2.24.1:")
    depends_on("r-biocgenerics@0.39.2:", type=("build", "run"), when="@2.28.0:")
    depends_on("r-s4vectors@0.13.17:", type=("build", "run"))
    depends_on("r-s4vectors@0.15.5:", type=("build", "run"), when="@2.12.0:")
    depends_on("r-s4vectors@0.18.2:", type=("build", "run"), when="@2.14.12:")
    depends_on("r-s4vectors@0.19.11:", type=("build", "run"), when="@2.16.0:")
    depends_on("r-s4vectors@0.21.9:", type=("build", "run"), when="@2.18.3:")
    depends_on("r-s4vectors@0.25.14:", type=("build", "run"), when="@2.22.2:")
    depends_on("r-s4vectors@0.27.12:", type=("build", "run"), when="@2.24.1:")
    depends_on("r-s4vectors@0.29.19:", type=("build", "run"), when="@2.28.0:")
    depends_on("r-s4vectors@0.33.3:", type=("build", "run"), when="@2.30.0:")
