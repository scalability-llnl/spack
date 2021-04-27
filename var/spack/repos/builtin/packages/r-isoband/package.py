# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RIsoband(RPackage):
    """Generate Isolines and Isobands from Regularly Spaced Elevation Grids

    A fast C++ implementation to generate contour lines (isolines) and contour
    polygons (isobands) from regularly spaced grids containing elevation
    data."""

    homepage = "https://github.com/wilkelab/isoband"
    url      = "https://cloud.r-project.org/src/contrib/isoband_0.2.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/isoband"

    version('0.2.3', sha256='f9d3318fdf6d147dc2e2c7015ea7de42a55fa33d6232b952f982df96066b7ffe')

    depends_on('r-testthat', type=('build', 'run'))
