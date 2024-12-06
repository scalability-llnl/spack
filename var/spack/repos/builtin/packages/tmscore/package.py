# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tmscore(Package):
    """TM-score is a metric for assessing the topological similarity of
    protein structures."""

    homepage = "https://zhanggroup.org/TM-score/"
    url = "https://zhanggroup.org/TM-score/TMscore.cpp"

    maintainers("snehring")

    version(
        "20220227",
        sha256="30274251f4123601af102cf6d4f1a9cc496878c1ae776702f554e2fc25658d7f",
        expand=False,
    )

    variant("fast-math", default=False, description="Enable fast math")

    phases = ["build", "install"]

    def build(self, spec, prefix):
        cxx = Executable(self.compiler.cxx)
        args = ["-O3"]
        if spec.satisfies("+fast-math"):
            args.append("-ffast-math")
        args.extend(["-lm", "-o", "TMscore", "TMscore.cpp"])
        cxx(*args)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("TMscore", prefix.bin)
