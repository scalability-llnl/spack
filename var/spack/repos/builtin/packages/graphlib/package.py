# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Graphlib(CMakePackage):
    """Library to create, manipulate, and export graphs Graphlib."""

    homepage = "https://github.com/LLNL/graphlib"
    url = "https://github.com/LLNL/graphlib/archive/v2.0.0.tar.gz"
    maintainers("lee218llnl")

    version("2.0.0", sha256="4f4aa1193167c41c8491dec3cf22b1e52a8f0842faab88b7945972f02d2adbcd")
    version("3.0.0", sha256="c3d889f7bc25b9662426605e52f14cd16f9c05b034738a343890707f5f5681f1")

    depends_on("c", type="build")  # generated

    depends_on("cmake@2.6:", type="build")
