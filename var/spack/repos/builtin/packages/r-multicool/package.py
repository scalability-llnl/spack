# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMulticool(RPackage):
    """Permutations of multisets in cool-lex order.

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
    <https://jeromekelleher.net/tag/integer-partitions.html>. The C++ code and
    Python code are distributed without conditions."""

    cran = "multicool"

    license("GPL-2.0-only")

    version("1.0.1", sha256="bd72de1fbd7ea32018d6af09ac2af80871ebe26bf9dfdf1ba53f87e6cff56c1f")
    version("0.1-12", sha256="487d28d9c3c606be0cf56e2d8f8b0d79fb71949c68886ea9251fbb1c01664a36")
    version("0.1-11", sha256="1c907e64af2ac39facdf431a5691e69649f64af1f50e198ae39da5bf30026476")
    version("0.1-10", sha256="5bb0cb0d9eb64420c862877247a79bb0afadacfe23262ec8c3fa26e5e34d6ff9")
    version("0.1-9", sha256="bdf92571cef1b649952d155395a92b8683099ee13114f73a9d41fc5d7d49d329")

    depends_on("r-rcpp@0.11.2:", type=("build", "run"))
