# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RForeach(RPackage):
    """Provides Foreach Looping Construct.

    Support for the foreach looping construct. Foreach is an idiom that allows
    for iterating over elements in a collection, without the use of an explicit
    loop counter. This package in particular is intended to be used for its
    return value, rather than for its side effects.  In that sense, it is
    similar to the standard lapply function, but doesn't require the evaluation
    of a function. Using foreach without side effects also facilitates
    executing the loop in parallel."""

    cran = "foreach"

    license("Apache-2.0")

    version("1.5.2", sha256="56338d8753f9f68f262cf532fd8a6d0fe25a71a2ff0107f3ce378feb926bafe4")
    version("1.5.1", sha256="fb5ad69e295618c52b2ac7dff84a0771462870a97345374d43b3de2dc31a68e1")
    version("1.4.7", sha256="95632c0b1182fc01490718d82fa3b2bce864f2a011ae53282431c7c2a3f5f160")
    version("1.4.3", sha256="1ef03f770f726a62e3753f2402eb26b226245958fa99d570d003fc9e47d35881")

    depends_on("r@2.5.0:", type=("build", "run"))
    depends_on("r-codetools", type=("build", "run"))
    depends_on("r-iterators", type=("build", "run"))
