# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RMisc3d(RPackage):
    """Miscellaneous 3D Plots

    A collection of miscellaneous 3d plots, including isosurfaces."""

    homepage = "https://cloud.r-project.org/package=misc3d"
    url      = "https://cloud.r-project.org/src/contrib/misc3d_0.8-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/misc3d"

    version('0.9-0', sha256='a1e9291d625bd1312bae5b0e26d48b9362f66a8a0fabbf48891ba1d2432e4e82')
    version('0.8-4', sha256='75de3d2237f67f9e58a36e80a6bbf7e796d43eb46789f2dd1311270007bf5f62')

    depends_on('r+X', type=('build', 'run'))
