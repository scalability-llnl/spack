# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RIntervals(RPackage):
    """Tools for Working with Points and Intervals

    Tools for working with and comparing sets of points and intervals."""

    homepage = "http://github.com/edzer/intervals"
    url      = "https://cloud.r-project.org/src/contrib/intervals_0.15.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/intervals"

    version('0.15.2', sha256='0bd23b0ce817ddd851238233d8a5420bf3a6d29e75fd361418cbc50118777c57')
    version('0.15.1', sha256='9a8b3854300f2055e1492c71932cc808b02feac8c4d3dbf6cba1c7dbd09f4ae4')

    depends_on('r@2.9.0:', type=('build', 'run'))
