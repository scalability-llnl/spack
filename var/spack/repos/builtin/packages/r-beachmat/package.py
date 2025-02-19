# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBeachmat(RPackage):
    """Compiling Bioconductor to Handle Each Matrix Type.

    Provides a consistent C++ class interface for reading from and writing
    data to a variety of commonly used matrix types. Ordinary matrices and
    several sparse/dense Matrix classes are directly supported, third-party
    S4 classes may be supported by external linkage, while all other
    matrices are handled by DelayedArray block processing."""

    bioc = "beachmat"

    version("2.22.0", commit="a1438568f8f83d73a4f5f3ec5b6cd7d4b6955e74")
    version("2.20.0", commit="fe0b11965d2192ae5ffab503e69f31ae0bc450b0")
    version("2.18.1", commit="39ef12f2aa1bbc2d057aa90c1964e67e8c5c5715")
    version("2.16.0", commit="4cc8e50dcae767a2ef84ffc7a581ea182f05f300")
    version("2.14.0", commit="5a4b85f4a22f3447f12d03157ab95de73f6137c6")
    version("2.12.0", commit="3e6af145bdcdf0a0b722d8256ba1a38b8a36b2f5")
    version("2.10.0", commit="b7cc532d4a5b26d9073135cc9945258ea08e5079")
    version("2.6.4", commit="7d9dc6379017d723dda3e8dc9fd1f6de7fd33cdb")
    version("2.0.0", commit="2bdac6ce7b636fd16f78641a0bcc2181670107ab")
    version("1.4.0", commit="e3b7a21cae0080d077a0d40e35d1d148f088720a")
    version("1.2.1", commit="ebae81772045a314e568c2f7d73ea3b27e7bf7d8")
    version("1.0.2", commit="6bd57b91d6428ac916f46572d685d3cb01a757f7")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.4:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@1.2.1:1.4.0")
    depends_on("r-delayedarray", type=("build", "run"))
    depends_on("r-delayedarray@0.5.30:", type=("build", "run"), when="@1.2.1")
    depends_on("r-delayedarray@0.7.38:", type=("build", "run"), when="@1.4.0")
    depends_on("r-delayedarray@0.15.14:", type=("build", "run"), when="@2.6.4")
    depends_on("r-delayedarray@0.27.2:", type=("build", "run"), when="@2.17.1:")
    depends_on("r-sparsearray", type=("build", "run"), when="@2.17.8:")
    depends_on("r-biocgenerics", type=("build", "run"), when="@1.4.0:")
    depends_on("r-matrix", type=("build", "run"), when="@2.6.4:")
    depends_on("r-rcpp@0.12.14:", type=("build", "run"), when="@1.0.2:")
    depends_on("r-rcpp", type=("build", "run"), when="@2.10.0:")
    depends_on("r-assorthead", type=("build", "run"), when="@2.21.6:")

    depends_on("r-rhdf5lib", type=("build", "run"), when="@1.0.2:1.4.0")
    depends_on("r-rhdf5lib@1.1.4:", type=("build", "run"), when="@1.2.1")
    depends_on("r-hdf5array", type=("build", "run"), when="@1.0.2:1.4.0")
    depends_on("r-hdf5array@1.7.3:", type=("build", "run"), when="@1.2.1")
    depends_on("r-hdf5array@1.9.5:", type=("build", "run"), when="@1.4.0")
    depends_on("r-rhdf5", type=("build", "run"), when="@1.0.2:1.4.0")
