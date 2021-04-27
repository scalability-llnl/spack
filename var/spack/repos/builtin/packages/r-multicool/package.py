# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RMulticool(RPackage):
    """Permutations of multisets in cool-lex order

    A set of tools to permute multisets without loops or hash tables and to
    generate integer partitions. The permutation functions are based on C code
    from Aaron Williams. Cool-lex order is similar to colexicographical order.
    The algorithm is described in Williams, A. (2009)
    <DOI:10.1145/1496770.1496877> Loopless Generation of Multiset Permutations
    by Prefix Shifts. Symposium on Discrete Algorithms, New York, United
    States. The permutation code is distributed without restrictions. The code
    for stable and efficient computation of multinomial coefficients comes from
    Dave Barber. The code can be download from
    <http://tamivox.org/dave/multinomial/code.html> and is distributed without
    conditions. The package also generates the integer partitions of a
    positive, non-zero integer n. The C++ code for this is based on Python code
    from Jerome Kelleher which can be found here
    <http://jeromekelleher.net/tag/integer-partitions.html>. The C++ code and
    Python code are distributed without conditions."""

    homepage = "https://cloud.r-project.org/package=multicool"
    url      = "https://cloud.r-project.org/src/contrib/Archive/multicool/multicool_0.1-9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/multicool/Archive/multicool"

    version('0.1-10', sha256='5bb0cb0d9eb64420c862877247a79bb0afadacfe23262ec8c3fa26e5e34d6ff9')
    version('0.1-9', sha256='bdf92571cef1b649952d155395a92b8683099ee13114f73a9d41fc5d7d49d329')

    depends_on('r-rcpp@0.11.2:', type=('build', 'run'))
