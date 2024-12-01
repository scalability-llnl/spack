# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tmalign(Package):
    """TM-align is an algorithm for sequence-order independent protein
    structure comparisons."""

    homepage = "https://zhanggroup.org/TM-align/"
    url = "https://zhanggroup.org/TM-align/TMalign.cpp"

    maintainers("snehring")

    version(
        "20220412",
        sha256="09227c46705ca8cf7c922a6e1672c34d7ed4daba32e5c7c484306808db54117a",
        expand=False,
    )
    version(
        "2016-05-25",
        sha256="ce7f68289f3766d525afb0a58e3acfc28ae05f538d152bd33d57f8708c60e2af",
        url="http://zhanglab.ccmb.med.umich.edu/TM-align/TM-align-C/TMalignc.tar.gz",
        deprecated=True,
    )

    variant("fast-math", default=False, description="Enable fast math", when="@20220412:")

    with when("@20220412:"):
        phases = ["build", "install"]

    def build(self, spec, prefix):
        cxx = Executable(self.compiler.cxx)
        args = ["-O3"]
        if spec.satisfies("+fast-math"):
            args.append("-ffast-math")
        args.extend(["-lm", "-o", "TMalign", "TMalign.cpp"])
        cxx(*args)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("TMalign", prefix.bin)
