# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRmpfr(RPackage):
    """Arithmetic (via S4 classes and methods) for arbitrary precision
       floating point numbers, including transcendental ("special")
       functions. To this end, Rmpfr interfaces to the LGPL'ed MPFR
       (Multiple Precision Floating-Point Reliable) Library which itself
       is based on the GMP (GNU Multiple Precision) Library."""

    homepage = "http://rmpfr.r-forge.r-project.org"
    url      = "https://cloud.r-project.org/src/contrib/Rmpfr_0.6-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Rmpfr"

    version('0.7-2', sha256='ec1da6ec5292ea6ac95495c6a299591d367e520ae324719817fb884c865603ff')
    version('0.7-1', sha256='9b3021617a22b0710b0f1acc279290762317ff123fd9e8fd03f1449f4bbfe204')
    version('0.6-1', sha256='bf50991055e9336cd6a110d711ae8a91a0551b96f9eaab5fef8c05f578006e1c')

    depends_on('r@3.0.1:', when='@:0.6-1', type=('build', 'run'))
    depends_on('r@3.1.0:', when='@0.7-0', type=('build', 'run'))
    depends_on('r@3.3.0:', when='@0.7-1:', type=('build', 'run'))
    depends_on('r-gmp@0.5-8:', type=('build', 'run'))
    depends_on('mpfr@3.0.0:')
    depends_on('gmp@4.2.3:')
