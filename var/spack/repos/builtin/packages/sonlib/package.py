# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Sonlib(MakefilePackage):
    """sonLib is a compact C/Python library for
    sequence analysis in bioinformatics."""

    # This is sonlib as needed by the hal package which expects
    # a side by side compilation
    #
    # If you need to use sonlib then you want py-sonlib

    homepage = "https://github.com/ComparativeGenomicsToolkit"
    url = "https://github.com/ComparativeGenomicsToolkit/sonLib"
    git = "https://github.com/ComparativeGenomicsToolkit/sonLib.git"

    license("MIT")

    version("master", branch="master")
    version("2020-04-01", commit="7ebe2ede05a6ee366d93a7a993db69a99943a68f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def setup_build_environment(self, env):
        binpath = os.path.join(self.stage.source_path, "bin")
        libpath = os.path.join(self.stage.source_path, "lib")

        env.set("BINDIR", binpath)
        env.set("LIBDIR", libpath)

    def build(self, spec, prefix):
        binpath = os.path.join(self.stage.source_path, "bin")
        libpath = os.path.join(self.stage.source_path, "lib")

        mkdir(binpath)
        mkdir(libpath)

        make()

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
