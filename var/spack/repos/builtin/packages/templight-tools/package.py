# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TemplightTools(CMakePackage):
    """Supporting tools for the Templight Profiler"""

    homepage = "https://github.com/mikael-s-persson/templight-tools"
    git = "https://github.com/mikael-s-persson/templight-tools.git"

    license("GPL-3.0-only")

    version("develop", branch="master")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake @2.8.7:", type="build")
    depends_on("boost @1.48.1: +exception+filesystem+system+graph+program_options+test+container")
