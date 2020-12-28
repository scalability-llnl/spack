# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgridges(RPackage):
    """Ridgeline plots provide a convenient way of visualizing changes in
    distributions over time or space."""

    homepage = "https://cloud.r-project.org/package=ggridges"
    url      = "https://cloud.r-project.org/src/contrib/ggridges_0.4.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggridges"

    version('0.5.1', sha256='01f87cdcdf2052ed9c078d9352465cdeda920a41e2ca55bc154c1574fc651c36')
    version('0.5.0', sha256='124bc84044e56728fa965682f8232fc868f2af7d3eb7276f6b0df53be8d2dbfe')
    version('0.4.1', sha256='03d2013df6adf07c9741d4476df96865b878a88359763ac36b98aa86591cca4d')
    version('0.4.0', sha256='c62153fb47f55468c873e6cf882b46754b6eedec423dacf3992ab23c474d521c')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-ggplot2@2.2.0:', type=('build', 'run'))
    depends_on('r-plyr@1.8.0:', type=('build', 'run'))
    depends_on('r-scales@0.4.1:', type=('build', 'run'))
    depends_on('r-withr@2.1.1:', when='@0.5.0:', type=('build', 'run'))
