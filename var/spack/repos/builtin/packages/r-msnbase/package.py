# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMsnbase(RPackage):
    """Base Functions and Classes for Mass Spectrometry and Proteomics.

    MSnbase provides infrastructure for manipulation, processing and
    visualisation of mass spectrometry and proteomics data, ranging from raw
    to quantitative and annotated data."""

    bioc = "MSnbase"

    version("2.26.0", commit="3e6268a86b93c474e37b21a9b8f564812202b2b6")
    version("2.24.0", commit="b96e0142c663c2cb01e92479816a503c46caa1a8")
    version("2.22.0", commit="4f6e5767eee91b2105781b494fcabcfed16eba2d")
    version("2.20.4", commit="c86ac8b341832f2b577f2153258c1abf064e6448")
    version("2.16.1", commit="4d88b4edd1af59474462b1b06ad0ec5831f3a878")
    version("2.10.1", commit="4d5899bc9c714f0b1a70cddd537cd4621b2b53b0")
    version("2.8.3", commit="ef883752c5e92d445647bc5b5d23d5df320db415")
    version("2.6.4", commit="46836860ce0281eef135303f2e2948303d67f68c")
    version("2.4.2", commit="c045d65daa730c7837852e6343a05cae9644ab5e")
    version("2.2.0", commit="d6e8fb7f106d05096fa9074da0f829ac8f02c197")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@2.16.1:")
    depends_on("r-biocgenerics@0.7.1:", type=("build", "run"))
    depends_on("r-biobase@2.15.2:", type=("build", "run"))
    depends_on("r-mzr@2.7.6:", type=("build", "run"))
    depends_on("r-mzr@2.11.11:", type=("build", "run"), when="@2.4.2:")
    depends_on("r-mzr@2.13.6:", type=("build", "run"), when="@2.6.4:")
    depends_on("r-mzr@2.15.1:", type=("build", "run"), when="@2.8.3:")
    depends_on("r-mzr@2.17.3:", type=("build", "run"), when="@2.10.1:")
    depends_on("r-mzr@2.19.6:", type=("build", "run"), when="@2.16.1:")
    depends_on("r-mzr@2.29.3:", type=("build", "run"), when="@2.22.0:")
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-protgenerics@1.5.1:", type=("build", "run"))
    depends_on("r-protgenerics@1.19.3:", type=("build", "run"), when="@2.16.1:")
    depends_on("r-protgenerics@1.25.1:", type=("build", "run"), when="@2.20.4:")
    depends_on("r-protgenerics@1.27.2:", type=("build", "run"), when="@2.22.0:")
    depends_on("r-protgenerics@1.29.1:", type=("build", "run"), when="@2.24.0:")
    depends_on("r-mscoreutils", type=("build", "run"), when="@2.20.4:")
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-iranges@2.13.28:", type=("build", "run"), when="@2.6.4:")
    depends_on("r-plyr", type=("build", "run"))
    depends_on("r-vsn", type=("build", "run"))
    depends_on("r-affy", type=("build", "run"))
    depends_on("r-impute", type=("build", "run"))
    depends_on("r-pcamethods", type=("build", "run"))
    depends_on("r-maldiquant@1.16:", type=("build", "run"))
    depends_on("r-mzid@1.5.2:", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-xml", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"), when="@2.6.4:")
    depends_on("r-mass", type=("build", "run"), when="@2.6.4:")
    depends_on("r-rcpp", type=("build", "run"))

    depends_on("r-preprocesscore", type=("build", "run"), when="@:2.16.1")
