# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcppcnpy(RPackage):
    """Read-Write Support for 'NumPy' Files via 'Rcpp'.

    The 'cnpy' library written by Carl Rogers provides read and write
    facilities for files created with (or for) the 'NumPy' extension for
    'Python'. Vectors and matrices of numeric types can be read or written to
    and from files as well as compressed files. Support for integer files is
    available if the package has been built with -std=c++11 which should be the
    default on all platforms since the release of R 3.3.0."""

    cran = "RcppCNPy"

    license("BitTorrent-1.0")

    version("0.2.12", sha256="856dbc857b2d425c80d9a1628e45743234fee2e68575aa9e2d29a6efae60c39a")
    version("0.2.11", sha256="5dbb36f2526c276fd79b8e08a30503dc401cdf54d8c40f61af758c9ee1192f55")
    version("0.2.10", sha256="77d6fbc86520a08da40d44c0b82767099f8f719ca95870d91efff1a9cab1ab9c")
    version("0.2.9", sha256="733f004ad1a8b0e5aafbf547c4349d2df3118afd57f1ff99f20e39135c6edb30")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("zlib-api")
