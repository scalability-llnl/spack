# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGmodels(RPackage):
    """Various R programming tools for model fitting."""

    homepage = "http://www.sf.net/projects/r-gregmisc"
    url      = "https://cloud.r-project.org/src/contrib/gmodels_2.16.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gmodels"

    version('2.18.1', sha256='626140a34eb8c53dd0a06511a76c71bc61c48777fa76fcc5e6934c9c276a1369')
    version('2.16.2', sha256='ab018894bdb376c5bd6bc4fbc4fe6e86590f4106795a586ef196fbb6699ec47d')

    depends_on('r@1.9.0:', type=('build', 'run'))
    depends_on('r-gdata', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
