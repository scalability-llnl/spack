# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnalysispageserver(RPackage):
    """A framework for sharing interactive data and plots from R through the
    web.

    AnalysisPageServer is a modular system that enables sharing of
    customizable R analyses via the web."""

    bioc = "AnalysisPageServer"

    version("1.18.1", commit="08bd85e872d3f2b0c1fa148cf30bcd2d1a29b630")
    version("1.16.0", commit="67b063523f80e2af1d26262367ff50f34e195174")
    version("1.14.0", commit="620c0ea1e129ddd1a0866e2c9d7c3fcf06a8baf4")
    version("1.12.0", commit="146501974ef1938ee1ec4eb293ea7eeca331a0dc")
    version("1.10.0", commit="876c87073be116fa15a1afdd407e21152eb80d50")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r-log4r", type=("build", "run"))
    depends_on("r-rjson", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-graph", type=("build", "run"))
