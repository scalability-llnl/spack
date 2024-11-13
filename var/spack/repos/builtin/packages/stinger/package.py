# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stinger(CMakePackage):
    """The STINGER in-memory graph store and dynamic graph analysis
    platform. Millions to billions of vertices and edges at thousands
    to millions of updates per second."""

    homepage = "http://www.stingergraph.com/"
    git = "https://github.com/stingergraph/stinger.git"

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    parallel = False

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree("./bin", prefix.bin)
            install_tree("./lib", prefix.lib)
            install_tree("./include", prefix.include)
            install_tree("./share", prefix.share)
