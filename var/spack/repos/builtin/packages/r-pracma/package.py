# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RPracma(RPackage):
    """Practical Numerical Math Functions

    Provides a large number of functions from numerical analysis and linear
    algebra, numerical optimization, differential equations, time series, plus
    some well-known special mathematical functions. Uses 'MATLAB' function
    names where appropriate to simplify porting."""

    homepage = "https://cloud.r-project.org/package=pracma"
    url      = "https://cloud.r-project.org/src/contrib/pracma_2.2.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pracma"

    version('2.2.9', sha256='0cea0ff5e88643df121e07b9aebfe57084c61e11801680039752f371fe87bf1e')

    depends_on('r@3.1.0:', type=('build', 'run'))
