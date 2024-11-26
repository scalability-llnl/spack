# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cotter(CMakePackage):
    """Andre Offringa's cotter pre-processing pipeline."""

    homepage = "https://github.com/MWATelescope/cotter"
    git = "https://github.com/MWATelescope/cotter.git"

    version("master", branch="master")
    version("20190205", commit="b7b07f3298a8d57b9dfff0b72fc21e68b23a42da")

    depends_on("cxx", type="build")  # generated

    depends_on("erfa")
    depends_on("pal")
    depends_on("aoflagger")
