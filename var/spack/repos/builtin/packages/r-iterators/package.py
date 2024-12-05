# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIterators(RPackage):
    """Provides Iterator Construct.

    Support for iterators, which allow a programmer to traverse through all the
    elements of a vector, list, or other collection of data."""

    cran = "iterators"

    license("Apache-2.0")

    version("1.0.14", sha256="cef3075a0930e1408c764e4da56bbadd4f7d14315809df8f38dd51f80ccc677b")
    version("1.0.13", sha256="778e30e4c292da9f94d62acc637cf55273dae258199d847e62658f44840f11a4")
    version("1.0.12", sha256="96bf31d60ebd23aefae105d9b7790715e63327eec0deb2ddfb3d543994ea9f4b")
    version("1.0.9", sha256="de001e063805fdd124953b571ccb0ed2838c55e40cca2e9d283d8a90b0645e9b")
    version("1.0.8", sha256="ae4ea23385776eb0c06c992a3da6b0256a6c84558c1061034c5a1fbdd43d05b8")

    depends_on("r@2.5.0:", type=("build", "run"))
