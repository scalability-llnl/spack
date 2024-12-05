# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTarifx(RPackage):
    """Collection of Utility and Convenience Functions.

    A collection of various utility and convenience functions."""

    cran = "taRifx"

    version("1.0.6.2", sha256="89d031db00a94ae57c7ace0d9aa39ba2f960f96fd48d2d1e4c7ebb62a2969b15")
    version("1.0.6.1", sha256="d4c832b26d476a395ddf8349c42613270023c8bbf52a274d280be6284c11d7e2")
    version("1.0.6", sha256="3dc70ac9c828d904cbac9fc9465918cd58cb5e9e35e92fe0cf38f436a1017782")

    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-plyr", type=("build", "run"))
