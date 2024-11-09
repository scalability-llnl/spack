# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiostrings(RPackage):
    """Efficient manipulation of biological strings.

    Memory efficient string containers, string matching algorithms, and
    other utilities, for fast manipulation of large biological sequences or
    sets of sequences."""

    bioc = "Biostrings"

    version("2.68.0", commit="f28b7838fb8321a9956506b3d2f4af2740bca124")
    version("2.66.0", commit="3470ca7da798971e2c3a595d8dc8d0d86f14dc53")
    version("2.64.1", commit="ffe263e958463bd1edb5d5d9316cfd89905be53c")
    version("2.64.0", commit="c7ad3c7af607bc8fe4a5e1c37f09e6c9bf70b4f6")
    version("2.62.0", commit="53ed287e03d16fa523789af3131c60375ccf587f")
    version("2.58.0", commit="0ec1a5455d5e9eebd14b26228906bb04e2abb197")
    version("2.52.0", commit="b78fe7c1f3cdbbb7affb1ca7164fe5a1f8b868f5")
    version("2.50.2", commit="025e734641a93f6c5d44243297cb4264ea0e34a2")
    version("2.48.0", commit="aa3599a7d259d658014d087b86d71ab1deb5f12b")
    version("2.46.0", commit="3bf6978c155498b50607d1bb471d1687d185a0fa")
    version("2.44.2", commit="e4a2b320fb21c5cab3ece7b3c6fecaedfb1e5200")

    depends_on("c", type="build")  # generated

    depends_on("r@2.8.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@2.50.2:")
    depends_on("r@4.0.0:", type=("build", "run"), when="@2.62.0:")
    # Older versions do not build with r@4.2:
    depends_on("r@:4.1", type=("build", "run"), when="@:2.62.0")
    depends_on("r-biocgenerics@0.15.6:", type=("build", "run"))
    depends_on("r-biocgenerics@0.31.5:", type=("build", "run"), when="@2.58.0:")
    depends_on("r-biocgenerics@0.37.0:", type=("build", "run"), when="@2.62.0:")
    depends_on("r-s4vectors@0.13.13:", type=("build", "run"))
    depends_on("r-s4vectors@0.17.25:", type=("build", "run"), when="@2.48.0:")
    depends_on("r-s4vectors@0.21.13:", type=("build", "run"), when="@2.52.0:")
    depends_on("r-s4vectors@0.27.12:", type=("build", "run"), when="@2.58.0:")
    depends_on("r-iranges@2.9.18:", type=("build", "run"), when="@2.44.2:")
    depends_on("r-iranges@2.13.24:", type=("build", "run"), when="@2.48.0:")
    depends_on("r-iranges@2.23.9:", type=("build", "run"), when="@2.58.0:")
    depends_on("r-iranges@2.30.1:", type=("build", "run"), when="@2.64.1:")
    depends_on("r-iranges@2.31.2:", type=("build", "run"), when="@2.66.0:")
    depends_on("r-xvector@0.11.6:", type=("build", "run"))
    depends_on("r-xvector@0.19.8:", type=("build", "run"), when="@2.48.0:")
    depends_on("r-xvector@0.21.4:", type=("build", "run"), when="@2.50.2:")
    depends_on("r-xvector@0.23.2:", type=("build", "run"), when="@2.52.0:")
    depends_on("r-xvector@0.29.2:", type=("build", "run"), when="@2.58.0:")
    depends_on("r-xvector@0.37.1:", type=("build", "run"), when="@2.66.0:")
    depends_on("r-genomeinfodb", type=("build", "run"), when="@2.62.0:")
    depends_on("r-crayon", type=("build", "run"), when="@2.58.0:")
