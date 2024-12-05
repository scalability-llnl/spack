# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDelayedarray(RPackage):
    """A unified framework for working transparently with on-disk and in-memory
    array-like datasets.

    Wrapping an array-like object (typically an on-disk object) in a
    DelayedArray object allows one to perform common array operations on it
    without loading the object in memory. In order to reduce memory usage
    and optimize performance, operations on the object are either delayed or
    executed using a block processing mechanism. Note that this also works
    on in-memory array-like objects like DataFrame objects (typically with
    Rle columns), Matrix objects, and ordinary arrays and data frames."""

    bioc = "DelayedArray"

    version("0.26.0", commit="e3bdae96838a8ed45f18697f072f3c4ec011aa03")
    version("0.24.0", commit="68ee3d0626c234ee1e9248a6cb95b901e4b3ad90")
    version("0.22.0", commit="4a5afd117b189b40bd409c7aff60e09d41797472")
    version("0.20.0", commit="829b52916ec54bb4f1a3c6f06c9955f3e28b3592")
    version("0.16.1", commit="c95eba771ad3fee1b49ec38c51cd8fd1486feadc")
    version("0.10.0", commit="4781d073110a3fd1e20c4083b6b2b0f260d0cb0a")
    version("0.8.0", commit="7c23cf46558de9dbe7a42fba516a9bb660a0f19f")
    version("0.6.6", commit="bdb0ac0eee71edd40ccca4808f618fa77f595a64")
    version("0.4.1", commit="ffe932ef8c255614340e4856fc6e0b44128a27a1")
    version("0.2.7", commit="909c2ce1665ebae2543172ead50abbe10bd42bc4")

    depends_on("c", type="build")  # generated

    depends_on("r@3.4:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@0.20.0:")
    depends_on("r-matrix", type=("build", "run"), when="@0.10.0:")
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-biocgenerics@0.25.1:", type=("build", "run"), when="@0.6.6:")
    depends_on("r-biocgenerics@0.27.1:", type=("build", "run"), when="@0.8.0:")
    depends_on("r-biocgenerics@0.31.5:", type=("build", "run"), when="@0.16.1:")
    depends_on("r-biocgenerics@0.37.0:", type=("build", "run"), when="@0.20.1:")
    depends_on("r-biocgenerics@0.43.4:", type=("build", "run"), when="@0.24.0:")
    depends_on("r-matrixgenerics@1.1.3:", type=("build", "run"), when="@0.16.1:")
    depends_on("r-s4vectors@0.14.3:", type=("build", "run"))
    depends_on("r-s4vectors@0.15.3:", type=("build", "run"), when="@0.4.1:")
    depends_on("r-s4vectors@0.17.43:", type=("build", "run"), when="@0.6.6:")
    depends_on("r-s4vectors@0.19.15:", type=("build", "run"), when="@0.8.0:")
    depends_on("r-s4vectors@0.21.7:", type=("build", "run"), when="@0.10.0:")
    depends_on("r-s4vectors@0.27.2:", type=("build", "run"), when="@0.16.1:")
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-iranges@2.11.17:", type=("build", "run"), when="@0.4.1:")
    depends_on("r-iranges@2.17.3:", type=("build", "run"), when="@0.10.0:")

    depends_on("r-matrixstats", type=("build", "run"), when="@:0.10.0")
    depends_on("r-biocparallel", type=("build", "run"), when="@0.6.6:0.10.0")
