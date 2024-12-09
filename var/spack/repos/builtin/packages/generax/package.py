# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Generax(CMakePackage):
    """GeneRax is a parallel tool for species tree-aware maximum likelihood
    based gene family tree inference under gene duplication, transfer,
    and loss.
    """

    homepage = "https://github.com/BenoitMorel/GeneRax"
    git = "https://github.com/BenoitMorel/GeneRax.git"

    maintainers("snehring")

    license("AGPL-3.0-or-later")

    version("master", branch="master", submodules=True)
    version("dev", branch="dev", submodules=True)
    version("2.0.4", commit="e4fab40f407bdd3b588d3d69a449f8c1be56f9fa", submodules=True)
    version("2.0.1", commit="0623dae55dd602a60faae63e9991fa8d41782456", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.0.1:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("bison")
    depends_on("flex")

    variant("mpi", default=False, description="Build with MPI support")

    build_directory = "build"

    patch("model-stdexcept.patch", when="@:2.0.4")

    def install(self, spec, prefix):
        install_tree("build/bin", prefix.bin)
