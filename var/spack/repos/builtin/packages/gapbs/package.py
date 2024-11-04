# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gapbs(MakefilePackage):
    """The GAP Benchmark Suite is intended to help graph processing research by
    standardizing evaluations. Fewer differences between graph processing
    evaluations will make it easier to compare different research efforts and
    quantify improvements. The benchmark not only specifies graph kernels,
    input graphs, and evaluation methodologies, but it also provides an
    optimized baseline implementation (this repo). These baseline
    implementations are representative of state-of-the-art performance, and
    thus new contributions should outperform them to demonstrate an
    improvement."""

    homepage = "http://gap.cs.berkeley.edu/benchmark.html"
    url = "https://github.com/sbeamer/gapbs/archive/v1.0.tar.gz"

    license("BSD-3-Clause")

    version("1.4", sha256="d91ecfe364e8c307e9e5535d730ef8ef8554b71d33891b70d0c4665cc11178bb")
    version("1.0", sha256="a7516998c4994592053c7aa0c76282760a8e009865a6b7a1c7c40968be1ca55d")

    depends_on("cxx", type="build")  # generated

    variant("serial", default=False, description="Version with no parallelism")

    def build(self, spec, prefix):
        cxx_flags = ["-O3", self.compiler.cxx11_flag]

        if spec.satisfies("-serial"):
            cxx_flags.append(self.compiler.openmp_flag)

        make("CXX_FLAGS=" + " ".join(cxx_flags))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        for app in ["bc", "bfs", "cc", "converter", "pr", "sssp", "tc"]:
            install(app, prefix.bin)
