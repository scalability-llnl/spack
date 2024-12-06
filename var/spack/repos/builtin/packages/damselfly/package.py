# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Damselfly(CMakePackage):
    """Damselfly is a model-based parallel network simulator."""

    homepage = "https://github.com/llnl/damselfly"
    url = "https://github.com/LLNL/damselfly/archive/v1.0.tar.gz"

    version("1.0", sha256="560e1b800c9036766396a1033c00914bd8d181b911e87140c3ac8879baf6545a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.6:", type="build")
    depends_on("mpi")
