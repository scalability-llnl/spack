# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qulacs(CMakePackage):
    """Qulacs is a Python/C++ library for fast simulation of large, noisy, or parametric quantum circuits.Qulacs is developed at QunaSys, Osaka University, NTT and Fujitsu."""

    homepage = "https://github.com/qulacs/qulacs"
    url = "https://github.com/qulacs/qulacs/archive/refs/tags/v0.5.5.tar.gz"
    maintainers = ["shigetoshisota","otsukay"]

    version("0.5.5", sha256="3a5dbb4a97528b5a33416f6f786e8793292c90bc99869379e45dbdde06e22b98")

    depends_on("boost@1.71.0:", type="build")
    depends_on("python@3.7.0:", type=("build", "run"))
    depends_on("cmake@3.0:", type="build")
    depends_on("eigen@3.3.7", type=("build", "link", "run"))
    depends_on("cereal@1.3.0", type="build")

    patch("v0.5.5.patch")
    patch("v0.5.5-fj.patch", when="%fj")
    patch("v0.5.5-gcc.patch", when="%gcc")

    def cmake(self, spec, prefix):
        bash = which("sh")
        if spec.satisfies("%fj"):
           bash("./script/build_fcc.sh")
        else:
           bash("./script/build_gcc.sh")

    def build(self, spec, prefix):
        return

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        mkdirp(prefix.include.Eigen)
        mkdirp(prefix.include.cereal)
        mkdirp(prefix.include.cereal.archives)
        mkdirp(prefix.include.cereal.details)
        mkdirp(prefix.include.cereal.external)
        mkdirp(prefix.include.cereal.types)
        mkdirp(prefix.include.cppsim)
        mkdirp(prefix.include.csim)
        mkdirp(prefix.include.gpusim)
        mkdirp(prefix.include.vqcsim)
        install("lib/*", prefix.lib)
        install("include/cppsim/*", prefix.include.cppsim)
        install("include/csim/*", prefix.include.csim)
        install("include/gpusim/*", prefix.include.gpusim)
        install("include/vqcsim/*", prefix.include.vqcsim)
