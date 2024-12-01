# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDelayedmatrixstats(RPackage):
    """Functions that Apply to Rows and Columns of 'DelayedMatrix' Objects.

    A port of the 'matrixStats' API for use with DelayedMatrix objects from
    the 'DelayedArray' package. High-performing functions operating on rows
    and columns of DelayedMatrix objects, e.g. col / rowMedians(), col /
    rowRanks(), and col / rowSds(). Functions optimized per data type and
    for subsetted calculations such that both memory usage and processing
    time is minimized."""

    bioc = "DelayedMatrixStats"

    version("1.22.0", commit="e820ab9a72963badc539e38fa79dbaeab95b2d2c")
    version("1.20.0", commit="1ed14250e8731e60bccb44946cafad4c2b3ac5b0")
    version("1.18.1", commit="9c4658d11fc20b7d88e05b9c52140c2ca8a65768")
    version("1.18.0", commit="50c9aab259b6e8f68abf44b78122662a41c8bf47")
    version("1.16.0", commit="d44a3d765769cb022193428a77af25bf19916be7")
    version("1.12.3", commit="2b3091dfa9b3bab914e3a4157182063714ba86ae")
    version("1.6.1", commit="4378d1898a403305a94b122c4f36d1215fa7708d")
    version("1.4.0", commit="eb5b390ef99651fe87a346848f807de95afe8971")
    version("1.2.0", commit="de868e730be6280dfad41a280ab09f4d3083c9ac")
    version("1.0.3", commit="e29a3444980ff727c5b12286884b06dfaebf5b5b")

    depends_on("r-matrixgenerics", type=("build", "run"), when="@1.12.2:")
    depends_on("r-matrixgenerics@1.5.3:", type=("build", "run"), when="@1.16.0:")
    depends_on("r-delayedarray", type=("build", "run"))
    depends_on("r-delayedarray@0.5.27:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-delayedarray@0.7.37:", type=("build", "run"), when="@1.4.0:")
    depends_on("r-delayedarray@0.9.8:", type=("build", "run"), when="@1.6.1:")
    depends_on("r-delayedarray@0.15.3:", type=("build", "run"), when="@1.12.2:")
    depends_on("r-delayedarray@0.17.6:", type=("build", "run"), when="@1.16.0:")
    depends_on("r-matrixstats@0.53.1:", type=("build", "run"))
    depends_on("r-matrixstats@0.55.0:", type=("build", "run"), when="@1.6.1:")
    depends_on("r-matrixstats@0.56.0:", type=("build", "run"), when="@1.12.2:")
    depends_on("r-matrixstats@0.60.0:", type=("build", "run"), when="@1.16.0:")
    depends_on("r-sparsematrixstats", type=("build", "run"), when="@1.12.2:")
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-matrix@1.5-0:", type=("build", "run"), when="@1.18.1:")
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-s4vectors@0.17.5:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-iranges@2.25.10:", type=("build", "run"), when="@1.16.0:")

    depends_on("r-hdf5array@1.7.10:", type=("build", "run"), when="@1.4.0:1.12.3")
    depends_on("r-hdf5array@1.17.2:", type=("build", "run"), when="@1.12.2:1.12.3")
    depends_on("r-biocparallel", type=("build", "run"), when="@1.4.0:1.12.3")
