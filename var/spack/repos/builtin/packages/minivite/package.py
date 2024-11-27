# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minivite(MakefilePackage):
    """miniVite is a proxy application that implements a single phase of
    Louvain method in distributed memory for graph community detection.
    """

    tags = ["proxy-app", "ecp-proxy-app"]

    homepage = "https://hpc.pnl.gov/people/hala/grappolo.html"
    git = "https://github.com/Exa-Graph/miniVite.git"

    license("BSD-3-Clause")

    version("develop", branch="master")
    version("1.0", tag="v1.0", commit="65ccaa8a4ec0b4bea516e2abdafbeb2f8a5f0c94")
    version("1.1", tag="v1.1", commit="23476d9d41eb8a17bf4108ac56852dacda89b253")

    depends_on("cxx", type="build")  # generated

    variant("openmp", default=True, description="Build with OpenMP support")
    variant("opt", default=True, description="Optimization flags")

    depends_on("mpi")

    @property
    def build_targets(self):
        targets = []
        cxxflags = ["-std=c++11 -g -DCHECK_NUM_EDGES -DPRINT_EXTRA_NEDGES"]
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
        if self.version >= Version("1.1"):
            install("miniVite", prefix.bin)
        elif self.version >= Version("1.0"):
            install("dspl", prefix.bin)
