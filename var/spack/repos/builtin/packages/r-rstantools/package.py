# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRstantools(RPackage):
    """rstantools: Tools for Developing R Packages Interfacing with 'Stan'"""

    homepage = "http://discourse.mc-stan.org/"
    url      = "https://cloud.r-project.org/src/contrib/rstantools_1.5.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rstantools"

    version('1.5.1', sha256='5cab16c132c12e84bd08e18cd6ef25ba39d67a04ce61015fc4490659c7cfb485')

    depends_on('pandoc', type='build')
