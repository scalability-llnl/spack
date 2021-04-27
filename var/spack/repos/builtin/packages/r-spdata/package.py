# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RSpdata(RPackage):
    """Datasets for Spatial Analysis

    Diverse spatial datasets for demonstrating, benchmarking and teaching
    spatial data analysis.  It includes R data of class sf (defined by the
    package 'sf'), Spatial ('sp'), and nb ('spdep'). Unlike other spatial data
    packages such as 'rnaturalearth' and 'maps',  it also contains data stored
    in a range of file formats including GeoJSON, ESRI Shapefile and
    GeoPackage.  Some of the datasets are designed to illustrate specific
    analysis techniques. cycle_hire() and cycle_hire_osm(), for example, is
    designed to illustrate point pattern analysis techniques."""

    homepage = "https://github.com/Nowosad/spData"
    url      = "https://cloud.r-project.org/src/contrib/spData_0.3.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spData"

    version('0.3.8', sha256='7a61268db4fdbfb004b77d36e953cbb3fdfdac7e8bb6c500628ec6c592c79ad6')
    version('0.3.0', sha256='de24ea659541a6c795cd26a1f6a213e15061af9c97a24cba1c24ce30c6c24c98')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-sp', when='@0.3.8:', type=('build', 'run'))
    depends_on('r-raster', when='@0.3.8:', type=('build', 'run'))
