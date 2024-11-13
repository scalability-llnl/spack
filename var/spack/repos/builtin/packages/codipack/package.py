# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Codipack(CMakePackage, Package):
    """CoDiPack is a C++-library that enables the computation of gradients in computer programs
    using Algorithmic Differentiation. It is based on the Operator Overloading approach and uses
    static polymorphism and expression templates, resulting in an extremely fast evaluation of
    adjoints or forward derivatives. It is specifically designed with HPC applications in mind."""

    homepage = "https://www.scicomp.uni-kl.de/software/codi/"
    url = "https://github.com/SciCompKL/CoDiPack/archive/refs/tags/v2.1.0.tar.gz"
    git = "https://github.com/SciCompKL/CoDiPack.git"

    version("2.2.0", sha256="24e9129829588fd8965620f275e40ae3a0be3b24015bc7d7280fa5ad551c10ac")
    version("2.1.0", sha256="c8d07eb01eaa056175902d5b153b8606b05d208ff0a541d15284f4d9ff6e87c2")
    version("2.0.2", sha256="c6eecfdbf5818daf80871461f23f8a29b5b72e314d2034047d0b0fcd44744339")
    version("1.9.3", sha256="27dd92d0b5132de37b431989c0c3d5bd829821a6a2e31e0529137e427421f06e")
    version("openmp", branch="experimentalOpenMPSupport")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.12:", type="build", when="@2.1.0:")

    build_system(
        conditional("cmake", when="@2.1.0:"),
        conditional("generic", when="@:2.0.2"),
        default="cmake",
    )


class GenericBuilder(spack.build_systems.generic.GenericBuilder):
    def install(self, pkg, spec, prefix):
        mkdirp(join_path(prefix, "include"))
        install_tree(join_path(self.stage.source_path, "include"), join_path(prefix, "include"))
