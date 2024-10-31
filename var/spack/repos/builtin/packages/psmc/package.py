# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Psmc(MakefilePackage):
    """mplementation of the Pairwise Sequentially Markovian Coalescent
    (PSMC) model"""

    homepage = "https://github.com/lh3/psmc"
    git = "https://github.com/lh3/psmc.git"

    license("MIT")

    version("2016-1-21", commit="e5f7df5d00bb75ec603ae0beff62c0d7e37640b9")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api", type="link")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin.utils)

    def build(self, spec, prefix):
        make()
        with working_dir("utils"):
            make()

    def install(self, spec, prefix):
        install_tree(self.build_directory, prefix.bin)
