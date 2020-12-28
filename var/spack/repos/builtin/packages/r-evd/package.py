# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REvd(RPackage):
    """evd: Functions for Extreme Value Distributions"""

    homepage = "https://cloud.r-project.org/package=evd"
    url      = "https://cloud.r-project.org/src/contrib/evd_2.3-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/evd"

    version('2.3-3', sha256='2fc5ef2e0c3a2a9392425ddd45914445497433d90fb80b8c363877baee4559b4')
