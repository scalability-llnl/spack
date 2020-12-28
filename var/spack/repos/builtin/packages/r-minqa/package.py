# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMinqa(RPackage):
    """Derivative-free optimization by quadratic approximation based on an
    interface to Fortran implementations by M. J. D. Powell."""

    homepage = "http://optimizer.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/minqa_1.2.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/minqa"

    version('1.2.4', sha256='cfa193a4a9c55cb08f3faf4ab09c11b70412523767f19894e4eafc6e94cccd0c')

    depends_on('r-rcpp@0.9.10:', type=('build', 'run'))
    depends_on('gmake', type='build')
