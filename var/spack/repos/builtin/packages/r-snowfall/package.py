# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSnowfall(RPackage):
    """Usability wrapper around snow for easier development of parallel R
       programs. This package offers e.g. extended error checks, and additional
       functions. All functions work in sequential mode, too, if no cluster is
       present or wished. Package is also designed as connector to the cluster
       management tool sfCluster, but can also used without it."""

    homepage = "https://cloud.r-project.org/package=snowfall"
    url      = "https://cloud.r-project.org/src/contrib/snowfall_1.84-6.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/snowfall"

    version('1.84-6.1', sha256='5c446df3a931e522a8b138cf1fb7ca5815cc82fcf486dbac964dcbc0690e248d')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-snow', type=('build', 'run'))
