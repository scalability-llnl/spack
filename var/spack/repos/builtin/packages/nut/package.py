# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nut(CMakePackage):
    """NuT is Monte Carlo code for neutrino transport and
    is a C++ analog to the Haskell McPhD code.
    NuT is principally aimed at exploring on-node parallelism
    and performance issues."""

    homepage = "https://github.com/lanl/NuT"
    url = "https://github.com/lanl/NuT/archive/0.1.1.tar.gz"
    git = "https://github.com/lanl/NuT.git"

    tags = ["proxy-app"]

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version("0.1.1", sha256="9f1dca4a9d7003b170fd57d6720228ff25471616cf884e033652e90c49c089bb")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.0:", type="build")
    depends_on("random123")

    # The conflict with %nvhpc is inherited from random123,
    # which is a C++ template library
    conflicts("%nvhpc")
    conflicts("%intel", when="@serial")
    conflicts("%pgi", when="@serial")
    conflicts("%xl", when="@serial")
    conflicts("%nag", when="@serial")
    build_targets = ["VERBOSE=on"]

    def setup_build_environment(self, env):
        env.set("RANDOM123_DIR", self.spec["random123"].prefix)

    def install(self, spec, prefix):
        install("README.md", prefix)
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        install(join_path(self.build_directory, "apps/bh-3"), prefix.bin)
        install(join_path(self.build_directory, "lib/libnut.a"), prefix.lib)
        install_tree("test/data", prefix.data)
        install_tree("lib", prefix.include)
