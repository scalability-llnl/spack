# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMapplots(RPackage):
    """mapplots: Data Visualisation on Maps"""

    homepage = "https://cloud.r-project.org/package=mapplots"
    url      = "https://cloud.r-project.org/src/contrib/mapplots_1.5.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mapplots"

    version('1.5.1', sha256='37e96d34f37922180e07bb63b4514e07d42eee5bbf0885b278286ee48cf142a3')

    depends_on('r@2.10.0:', type=('build', 'run'))
