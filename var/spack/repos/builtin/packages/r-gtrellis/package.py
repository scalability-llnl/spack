# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGtrellis(RPackage):
    """Genome Level Trellis Layout.

    Genome level Trellis graph visualizes genomic data conditioned by
    genomic categories (e.g. chromosomes). For each genomic category,
    multiple dimensional data which are represented as tracks describe
    different features from different aspects. This package provides high
    flexibility to arrange genomic categories and to add self-defined
    graphics in the plot."""

    bioc = "gtrellis"

    license("MIT")

    version("1.32.0", commit="4c2361bde90a556aa5a585d45f056b3ddc806f9b")
    version("1.30.0", commit="da93b30ef812e231c47aa83da5c521f1801b3d14")
    version("1.28.0", commit="d770a7b3441e4003869c88cfd8e21fd6508b86c4")
    version("1.26.0", commit="f2c3121b31ad1b422e2cf503435d0590e903ff3f")
    version("1.22.0", commit="c071c5631f3dedda212aed87d9c02954b5ed6611")
    version("1.16.1", commit="a9003ededc8f2a48c78d4545e2f214023c13a7da")
    version("1.14.0", commit="93935fb34211d12b250e22291712e18a31b0208d")
    version("1.12.1", commit="7f3941adddbbfa17f4cf474b703568678a38272d")
    version("1.11.1", commit="ff47d99743fd697d5c724f7bb18131dfe76dee71")
    version("1.8.0", commit="f813b420a008c459f63a2a13e5e64c5507c4c472")

    depends_on("r@3.1.2:", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-circlize@0.3.3:", type=("build", "run"))
    depends_on("r-circlize@0.4.8:", type=("build", "run"), when="@1.16.1")
    depends_on("r-getoptlong", type=("build", "run"))
