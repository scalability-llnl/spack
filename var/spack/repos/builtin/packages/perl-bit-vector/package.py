# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBitVector(PerlPackage):
    """Efficient bit vector, set of integers and "big int" math library"""

    homepage = "http://search.cpan.org/~stbey/Bit-Vector-7.4/Vector.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/S/ST/STBEY/Bit-Vector-7.4.tar.gz"

    version('7.4', sha256='3c6daa671fecfbc35f92a9385b563d65f50dfc6bdc8b4805f9ef46c0d035a926')

    depends_on('perl-carp-clan', type=('build', 'run'))
