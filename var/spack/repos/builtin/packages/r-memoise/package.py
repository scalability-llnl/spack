# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMemoise(RPackage):
    """'Memoisation' of Functions.

    Cache the results of a function so that when you call it again with the
    same arguments it returns the pre-computed value."""

    cran = "memoise"

    license("MIT")

    version("2.0.1", sha256="f85034ee98c8ca07fb3cd826142c1cd1e1e5747075a94c75a45783bbc4fe2deb")
    version("1.1.0", sha256="b276f9452a26aeb79e12dd7227fcc8712832781a42f92d70e86040da0573980c")
    version("1.0.0", sha256="fd1b6cf12929890db7819f74a44a1dbe3d6f25c8a608a956d827f8be2f6c026b")

    depends_on("r-rlang@0.4.10:", type=("build", "run"), when="@2.0.1:")
    depends_on("r-cachem", type=("build", "run"), when="@2.0.1:")

    depends_on("r-digest@0.6.3:", type=("build", "run"), when="@:1.1.0")
