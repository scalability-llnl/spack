# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStargazer(RPackage):
    """stargazer: Well-Formatted Regression and Summary Statistics Tables"""

    homepage = "https://cloud.r-project.org/package=stargazer"
    url      = "https://cloud.r-project.org/src/contrib/stargazer_5.2.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/stargazer"

    version('5.2.2', sha256='70eb4a13a6ac1bfb35af07cb8a63d501ad38dfd9817fc3fba6724260b23932de')
