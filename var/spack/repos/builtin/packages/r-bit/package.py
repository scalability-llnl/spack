# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBit(RPackage):
    """Classes and Methods for Fast Memory-Efficient Boolean Selections.

    Provided are classes for boolean and skewed boolean vectors, fast boolean
    methods, fast unique and non-unique integer sorting, fast set operations on
    sorted and unsorted sets of integers, and foundations for ff (range index,
    compression, chunked processing)."""

    cran = "bit"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("4.0.5", sha256="f0f2536a8874b6a30b80baefbc68cb21f0ffbf51f3877bda8038c3f9f354bfbc")
    version("4.0.4", sha256="e404841fbe4ebefe4ecd4392effe673a8c9fa05f97952c4ce6e2f6159bd2f168")
    version("1.1-14", sha256="5cbaace1fb643a665a6ca69b90f7a6d624270de82420ca7a44f306753fcef254")
    version("1.1-12", sha256="ce281c87fb7602bf1a599e72f3e25f9ff7a13e390c124a4506087f69ad79d128")

    depends_on("c", type="build")  # generated

    depends_on("r@2.9.2:", type=("build", "run"))
