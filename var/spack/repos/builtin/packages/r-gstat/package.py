# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGstat(RPackage):
    """Spatial and Spatio-Temporal Geostatistical Modelling, Predictionand
    Simulation.

    Variogram modelling; simple, ordinary and universal point or block
    (co)kriging; spatio-temporal kriging; sequential Gaussian or indicator
    (co)simulation; variogram and variogram map plotting utility functions;
    supports sf and stars."""

    cran = "gstat"

    version('2.0-8', sha256='57cb9e8235a39379a96af0a5651c82e02fdd608375917939948c3dbf170668e8')
    version('2.0-6', sha256='6711e68aa2444cf2927879a03a976d8caeca5eac98d806b19a6a7178b90bfcab')
    version('2.0-3', sha256='20a93fe6bf89221a5888de273bddf9a98187806d507cd3cd6297c2b13e7acce1')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-sp@0.9-72:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-spacetime@1.0-0:', type=('build', 'run'))
    depends_on('r-fnn', type=('build', 'run'))
