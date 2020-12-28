# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGstat(RPackage):
    """gstat: Spatial and Spatio-Temporal Geostatistical Modelling,
       Predictionand Simulation"""

    homepage = "https://github.com/r-spatial/gstat/"
    url      = "https://cloud.r-project.org/src/contrib/gstat_2.0-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gstat"

    version('2.0-3', sha256='20a93fe6bf89221a5888de273bddf9a98187806d507cd3cd6297c2b13e7acce1')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-fnn', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-sp@0.9-72:', type=('build', 'run'))
    depends_on('r-spacetime@1.0-0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
