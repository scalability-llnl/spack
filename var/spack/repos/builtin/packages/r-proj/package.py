# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RProj(RPackage):
    """Generic Coordinate System Transformations Using 'PROJ'

    Currently non-operational, a harmless wrapper to allow package 'reproj' to
    install and function while relying on the 'proj4' package."""

    homepage = "https://github.com/hypertidy/PROJ"
    url      = "https://cloud.r-project.org/src/contrib/PROJ_0.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/PROJ"

    version('0.4.0', sha256='dde90cfeca83864e61a7422e1573d2d55bb0377c32b9a8f550f47b8631121ce7')
    version('0.1.0', sha256='5186f221335e8092bbcd4d82bd323ee7e752c7c9cf83d3f94e4567e0b407aa6f')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r@3.0.2:', when='@0.4.0:', type=('build', 'run'))
