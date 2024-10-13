# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Kahip(CMakePackage):
    """KaHIP - Karlsruhe High Quality Partitioning - is a family of graph
    partitioning programs. It includes KaFFPa (Karlsruhe Fast Flow
    Partitioner), which is a multilevel graph partitioning algorithm,
    in its variants Strong, Eco and Fast, KaFFPaE (KaFFPaEvolutionary)
    which is a parallel evolutionary algorithm that uses KaFFPa to
    provide combine and mutation operations, as well as KaBaPE which
    extends the evolutionary algorithm. Moreover, specialized
    techniques are included to partition road networks (Buffoon), to
    output a vertex separator from a given partition or techniques
    geared towards efficient partitioning of social networks.
    """

    homepage = "http://algo2.iti.kit.edu/documents/kahip/index.html"
    url = "https://github.com/KaHIP/KaHIP/archive/v3.14.tar.gz"
    git = "https://github.com/KaHIP/KaHIP.git"
    maintainers("ma595")

    license("MIT")

    version("develop", branch="master")
    version("3.14", sha256="9da04f3b0ea53b50eae670d6014ff54c0df2cb40f6679b2f6a96840c1217f242")
    version("3.13", sha256="fae21778a4ce8e59ccb98e5cbb6c01f0af7e594657d21f6c0eb2c6e74398deb1")
    version("3.12", sha256="df923b94b552772d58b4c1f359b3f2e4a05f7f26ab4ebd00a0ab7d2579f4c257")
    version("3.11", sha256="347575d48c306b92ab6e47c13fa570e1af1e210255f470e6aa12c2509a8c13e3")
    version(
        "2.00",
        sha256="1cc9e5b12fea559288d377e8b8b701af1b2b707de8e550d0bda18b36be29d21d",
        url="https://algo2.iti.kit.edu/schulz/software_releases/KaHIP_2.00.tar.gz",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "deterministic",
        default=False,
        when="@3.13:",
        description="Compile with the deterministic seed",
    )
    variant("metis", default=False, description="metis support")

    depends_on("scons", type="build", when="@2:2.10")
    depends_on("argtable")
    depends_on("mpi")  # Note: upstream package only tested on openmpi
    depends_on("metis", when="@3.12: +metis")

    conflicts("%apple-clang")
    conflicts("%clang")

    # Fix SConstruct files to be python3 friendly (convert print from a
    # statement to a function)
    # Split into 2 patch files:
    # *) first file patches Sconstruct files present in all versions (from
    # 2.00 to 2.10)
    # *) second is for files only present in 2.00
    patch("fix-sconstruct-for-py3.patch", when="@2:2.10 ^python@3:")
    patch("fix-sconstruct-for-py3-v2.00.patch", when="@2.00 ^python@3:")

    patch("cstdint.patch", when="@3:")

    # 'when' decorators to override new CMake build approach (old build was SConstruct).
    @when("@:2.10")
    def patch(self):
        """Internal compile.sh scripts hardcode number of cores to build with.
        Filter these out so Spack can control it."""

        files = [
            "compile.sh",
            "parallel/modified_kahip/compile.sh",
            "parallel/parallel_src/compile.sh",
        ]

        for f in files:
            filter_file("NCORES=.*", "NCORES={0}".format(make_jobs), f)

    @when("@3.13:")
    def cmake_args(self):
        return [self.define_from_variant("DETERMINISTIC_PARHIP", "deterministic")]

    @when("@:2.10")
    def cmake(self, spec, prefix):
        pass

    @when("@:2.10")
    def build(self, spec, prefix):
        """Build using the KaHIP compile.sh script. Uses scons internally."""
        builder = Executable("./compile.sh")
        builder()

    @when("@:2.10")
    def install(self, spec, prefix):
        """Install under the prefix"""
        # Ugly: all files land under 'deploy' and we need to disentangle them
        mkdirp(prefix.bin)
        mkdirp(prefix.include)
        mkdirp(prefix.lib)

        with working_dir("deploy"):
            for f in os.listdir("."):
                if re.match(r".*\.(a|so|dylib)$", f):
                    install(f, prefix.lib)
                elif re.match(r".*\.h$", f):
                    install(f, prefix.include)
                else:
                    install(f, prefix.bin)
