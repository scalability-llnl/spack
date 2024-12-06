# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCner(RPackage):
    """CNE Detection and Visualization.

    Large-scale identification and advanced visualization of sets of
    conserved noncoding elements."""

    bioc = "CNEr"

    version("1.36.0", commit="4f2feeb395cfc071ed97ba8b6327425dfd42d6b5")
    version("1.34.0", commit="878de98d18f6f959ad5e014ecd8165d3105d8b48")
    version("1.32.0", commit="1c92f3d7f3dccf76ab7d54f286117b09bc470b8f")
    version("1.30.0", commit="e682f2a7c8ebb561c872cf51a58ba36eed341187")
    version("1.26.0", commit="e5e582da6feeae0618c4460f16ece724215e3b20")
    version("1.20.0", commit="9c25d8e8f6f5fd8a5311f554c86e7ca1140a4ca5")
    version("1.18.1", commit="66aa88af04364c81832f3b09bad898f3c117f606")
    version("1.16.1", commit="a2bec4b98d5938709f959a69c151f553ef357941")
    version("1.14.0", commit="b8634d65c51728c815127e22b45eba7c9b9db897")
    version("1.12.1", commit="90d611f9cd19a73d0fe92ab03ef428519d64c017")

    depends_on("c", type="build")  # generated

    depends_on("r@3.2.2:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@1.14.0:")
    depends_on("r-biostrings@2.33.4:", type=("build", "run"))
    depends_on("r-dbi@0.6:", type=("build", "run"))
    depends_on("r-dbi@0.7:", type=("build", "run"), when="@1.14.0:")
    depends_on("r-rsqlite@0.11.4:", type=("build", "run"))
    depends_on("r-genomeinfodb@1.1.3:", type=("build", "run"))
    depends_on("r-genomicranges@1.23.16:", type=("build", "run"))
    depends_on("r-rtracklayer@1.25.5:", type=("build", "run"))
    depends_on("r-xvector@0.5.4:", type=("build", "run"))
    depends_on("r-genomicalignments@1.1.9:", type=("build", "run"))
    depends_on("r-s4vectors@0.13.13:", type=("build", "run"))
    depends_on("r-iranges@2.5.27:", type=("build", "run"))
    depends_on("r-readr@0.2.2:", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-reshape2@1.4.1:", type=("build", "run"))
    depends_on("r-ggplot2@2.1.0:", type=("build", "run"))
    depends_on("r-powerlaw@0.60.3:", type=("build", "run"))
    depends_on("r-annotate@1.50.0:", type=("build", "run"))
    depends_on("r-go-db@3.3.0:", type=("build", "run"))
    depends_on("r-r-utils@2.3.0:", type=("build", "run"))
    depends_on("r-keggrest@1.14.0:", type=("build", "run"))
    depends_on("zlib-api")
