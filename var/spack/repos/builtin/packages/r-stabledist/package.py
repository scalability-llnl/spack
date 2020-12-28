# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStabledist(RPackage):
    """Density, Probability and Quantile functions, and random number
    generation for (skew) stable distributions, using the parametrizations of
    Nolan."""

    homepage = "http://www.rmetrics.org/"
    url      = "https://cloud.r-project.org/src/contrib/stabledist_0.7-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/stabledist"

    version('0.7-1', sha256='06c5704d3a3c179fa389675c537c39a006867bc6e4f23dd7e406476ed2c88a69')

    depends_on('r@3.1.0:', type=('build', 'run'))
