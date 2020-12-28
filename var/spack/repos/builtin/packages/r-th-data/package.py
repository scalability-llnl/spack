# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RThData(RPackage):
    """Contains data sets used in other packages Torsten Hothorn maintains."""

    homepage = "https://cloud.r-project.org/package=TH.data"
    url      = "https://cloud.r-project.org/src/contrib/TH.data_1.0-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/TH.data"

    version('1.0-10', sha256='618a1c67a30536d54b1e48ba3af46a6edcd6c2abef17935b5d4ba526a43aff55')
    version('1.0-9', sha256='d8318a172ce2b9f7f284dc297c8a8d5093de8eccbb566c8e7580e70938dfae0f')
    version('1.0-8', sha256='478f109fcc1226500ead8e3bd6e047cecde2294fde4df8ec216d38313db79a9d')
    version('1.0-7', sha256='29e126344daccbebc7df68924730ae4159a0faad77f86302070920684ba6070e')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
