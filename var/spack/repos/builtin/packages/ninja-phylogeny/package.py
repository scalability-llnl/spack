# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NinjaPhylogeny(MakefilePackage):
    """NINJA is software for inferring large-scale neighbor-joining phylogenies."""

    homepage = "https://wheelerlab.org/software/ninja/"
    url = "https://github.com/TravisWheelerLab/NINJA/archive/refs/tags/0.98-cluster_only.tar.gz"

    maintainers("snehring")

    license("MIT")

    version("0.98", sha256="55675e1a9d51eddb3decc9a7570b6bcddb12e8a922cf1ca0a1ea43995793c9db")

    depends_on("cxx", type="build")  # generated

    build_directory = "NINJA"

    def edit(self, spec, prefix):
        with working_dir("NINJA"):
            filter_file(r"^CXX = g\+\+.*$", "", "Makefile")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir("NINJA"):
            install("Ninja", prefix.bin)
