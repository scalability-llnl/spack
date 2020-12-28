# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProj(RPackage):
    """A wrapper around the generic coordinate transformation software 'PROJ'
    that transforms geospatial coordinates from one coordinate reference system
    ('CRS') to another. This includes cartographic projections as well as
    geodetic transformations. Version 6.0.0 or higher is required. The
    intention is for this package to be used by user-packages such as 'reproj',
    and that the older 'PROJ.4' and version 5 pathways be provided by the
    legacy package. The 'PROJ' library is available from
    <https://proj.org/>."""

    homepage = "https://github.com/hypertidy/PROJ"
    url      = "https://cloud.r-project.org/src/contrib/PROJ_0.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/PROJ"

    version('0.1.0', sha256='5186f221335e8092bbcd4d82bd323ee7e752c7c9cf83d3f94e4567e0b407aa6f')

    depends_on('r@2.10:', type=('build', 'run'))

    depends_on('proj@6:')
