# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIterpc(RPackage):
    """Efficient Iterator for Permutations and Combinations.

    Iterator for generating permutations and combinations. They can be either
    drawn with or without replacement, or with distinct/ non-distinct items
    (multiset). The generated sequences are in lexicographical order
    (dictionary order). The algorithms to generate permutations and
    combinations are memory efficient. These iterative algorithms enable users
    to process all sequences without putting all results in the memory at the
    same time. The algorithms are written in C/C++ for faster performance.
    Note: 'iterpc' is no longer being maintained. Users are recommended to
    switch to 'arrangements'."""

    cran = "iterpc"

    license("GPL-2.0-only")

    version("0.4.2", sha256="38bd464042a27536f676e889263eb2c257a431b59083f58cb54473f42ba2071b")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-iterators", type=("build", "run"))
    depends_on("r-gmp@0.5-12:", type=("build", "run"))
    depends_on("r-arrangements@1.0.0:", type=("build", "run"))
