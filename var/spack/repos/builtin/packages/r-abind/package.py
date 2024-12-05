# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAbind(RPackage):
    """
    Combine Multidimensional Arrays.

    Combine multidimensional arrays into a single array. This is a
    generalization of 'cbind' and 'rbind'. Works with vectors, matrices, and
    higher-dimensional arrays. Also provides functions 'adrop', 'asub', and
    'afill' for manipulating, extracting and replacing data in arrays."""

    cran = "abind"

    license("LGPL-2.0-or-later")

    version("1.4-5", sha256="3a3ace5afbcb86e56889efcebf3bf5c3bb042a282ba7cc4412d450bb246a3f2c")
    version("1.4-3", sha256="b6c255878c1ab81701ae701f34546e88be115629b984ac4272e311fa3c0ea6ce")

    depends_on("r@1.5.0:", type=("build", "run"))
