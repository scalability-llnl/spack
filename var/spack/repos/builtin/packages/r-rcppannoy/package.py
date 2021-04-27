# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRcppannoy(RPackage):
    """'Rcpp' Bindings for 'Annoy', a Library for Approximate Nearest Neighbors

    'Annoy' is a small C++ library for Approximate Nearest Neighbors written
    for efficient memory usage as well an ability to load from / save to disk.
    This package provides an R interface by relying on the 'Rcpp' package,
    exposing the same interface as the original Python wrapper to 'Annoy'. See
    <https://github.com/spotify/annoy> for more on 'Annoy'. 'Annoy' is released
    under Version 2.0 of the Apache License. Also included is a small Windows
    port of 'mmap' which is released under the MIT license."""

    homepage = "https://cloud.r-project.org/package=RcppAnnoy"
    url      = "https://cloud.r-project.org/src/contrib/RcppAnnoy_0.0.12.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RcppAnnoy"

    version('0.0.18', sha256='e4e7ddf071109b47b4fdf285db6d2155618ed73da829c30d8e64fc778e63c858')
    version('0.0.12', sha256='8f736cbbb4a32c80cb08ba4e81df633846d725f27867e983af2012966eac0eac')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-rcpp@0.11.3:', type=('build', 'run'))
