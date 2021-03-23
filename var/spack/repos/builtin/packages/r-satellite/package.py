# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSatellite(RPackage):
    """Handling and Manipulating Remote Sensing Data

    Herein, we provide a broad variety of functions which are useful for
    handling, manipulating, and visualizing satellite-based remote sensing
    data. These operations range from mere data import and layer handling (eg
    subsetting), over Raster* typical data wrangling (eg crop, extend), to more
    sophisticated (pre-)processing tasks typically applied to satellite imagery
    (eg atmospheric and topographic correction). This functionality is
    complemented by a full access to the satellite layers' metadata at any
    stage and the documentation of performed actions in a separate log file.
    Currently available sensors include Landsat 4-5 (TM), 7 (ETM+), and 8
    (OLI/TIRS Combined), and additional compatibility is ensured for the
    Landsat Global Land Survey data set."""

    cran     = "satellite"

    version('1.0.2', sha256='6447476bd31216e5abe504221e465677954d07419b4174ab4f4e4f7a197969c5')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-rcpp@0.10.3:', type=('build', 'run'))
