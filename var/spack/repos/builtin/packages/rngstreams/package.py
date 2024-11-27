# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rngstreams(AutotoolsPackage):
    """Multiple independent streams of pseudo-random numbers."""

    homepage = "https://statmath.wu.ac.at/software/RngStreams"
    url = "https://statmath.wu.ac.at/software/RngStreams/rngstreams-1.0.1.tar.gz"

    license("GPL-3.0-only")

    version("1.0.1", sha256="966195febb9fb9417e4e361948843425aee12efc8b4e85332acbcd011ff2d9b0")

    depends_on("c", type="build")  # generated
