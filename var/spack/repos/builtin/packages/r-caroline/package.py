# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCaroline(RPackage):
    """caroline: A Collection of Database, Data Structure, Visualization,
       andUtility Functions for R"""

    homepage = "https://cloud.r-project.org/package=caroline"
    url      = "https://cloud.r-project.org/src/contrib/caroline_0.7.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/caroline"

    version('0.7.6', sha256='e7ba948f7d87f091b498dd0eec2ca4fdad7af4e2bbb67e0945c2f0d3f2eadda9')

    depends_on('r@1.8.0:', type=('build', 'run'))
