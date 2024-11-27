# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReshape(RPackage):
    """Flexibly Reshape Data.

    Flexibly restructure and aggregate data using just two functions: melt and
    cast."""

    cran = "reshape"

    license("MIT")

    version("0.8.9", sha256="791178b3b5f30c166ebf5910a5ab1c67b54e7023b10b6c2e2ddd1cc02a1e4048")
    version("0.8.8", sha256="4d5597fde8511e8fe4e4d1fd7adfc7ab37ff41ac68c76a746f7487d7b106d168")
    version("0.8.7", sha256="2fa6c87d1e89f182e51bc5a4fcda3d42d83b8fb4474ca525fa7a8db5081f3992")

    depends_on("r@2.6.1:", type=("build", "run"))
    depends_on("r-plyr", type=("build", "run"))
