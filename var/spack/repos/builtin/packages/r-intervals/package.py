# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIntervals(RPackage):
    """intervals: Tools for Working with Points and Intervals"""

    homepage = "http://github.com/edzer/intervals"
    url      = "https://cloud.r-project.org/src/contrib/intervals_0.15.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/intervals"

    version('0.15.1', sha256='9a8b3854300f2055e1492c71932cc808b02feac8c4d3dbf6cba1c7dbd09f4ae4')

    depends_on('r@2.9.0:', type=('build', 'run'))
