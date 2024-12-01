# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Neve(MakefilePackage):
    """Benchmark to study communication and memory-access performance of graphs."""

    homepage = "https://github.com/ECP-ExaGraph"
    git = "https://github.com/ECP-ExaGraph/neve.git"

    license("BSD-3-Clause")

    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    variant("openmp", default=True, description="Build with OpenMP support")
    variant("opt", default=True, description="Optimization flags")

    depends_on("mpi")

    @property
    def build_targets(self):
        targets = []
        cxxflags = ["-std=c++11 -g"]
        ldflags = []

        if "+openmp" in self.spec:
            cxxflags.append(self.compiler.openmp_flag)
            ldflags.append(self.compiler.openmp_flag)
        if "+opt" in self.spec:
            cxxflags.append(" -O3 ")

        targets.append("CXXFLAGS={0}".format(" ".join(cxxflags)))
        targets.append("OPTFLAGS={0}".format(" ".join(ldflags)))
        targets.append("CXX={0}".format(self.spec["mpi"].mpicxx))

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("neve", prefix.bin)
