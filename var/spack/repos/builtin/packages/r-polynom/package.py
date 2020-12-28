# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPolynom(RPackage):
    """A collection of functions to implement a class for univariate polynomial
    manipulations."""

    homepage = "https://cloud.r-project.org/package=polynom"
    url      = "https://cloud.r-project.org/src/contrib/polynom_1.4-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/polynom"

    version('1.4-0', sha256='c5b788b26f7118a18d5d8e7ba93a0abf3efa6603fa48603c70ed63c038d3d4dd')
