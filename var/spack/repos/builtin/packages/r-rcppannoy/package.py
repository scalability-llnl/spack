# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcppannoy(RPackage):
    """'Rcpp' Bindings for 'Annoy', a Library for Approximate Nearest
    Neighbors.

    'Annoy' is a small C++ library for Approximate Nearest Neighbors written
    for efficient memory usage as well an ability to load from / save to disk.
    This package provides an R interface by relying on the 'Rcpp' package,
    exposing the same interface as the original Python wrapper to 'Annoy'. See
    <https://github.com/spotify/annoy> for more on 'Annoy'. 'Annoy' is released
    under Version 2.0 of the Apache License. Also included is a small Windows
    port of 'mmap' which is released under the MIT license."""

    cran = "RcppAnnoy"

    version("0.0.22", sha256="9f2121d787c4d3e7beccdd65f5d1de81f31c99d57d5d61ca3cc5af7169dd8f65")
    version("0.0.20", sha256="dcc6c7e091154d0a5698472e0fc7ed77976941c7376d21e019c90c3efaeacf85")
    version("0.0.19", sha256="89b209900516f3096b53c90937081fb8965c605c867aa465f1b3b68092b7688a")
    version("0.0.18", sha256="e4e7ddf071109b47b4fdf285db6d2155618ed73da829c30d8e64fc778e63c858")
    version("0.0.12", sha256="8f736cbbb4a32c80cb08ba4e81df633846d725f27867e983af2012966eac0eac")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rcpp@0.11.3:", type=("build", "run"), when="@:0.0.12")
