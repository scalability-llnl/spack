# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hybpiper(PythonPackage, Package):
    """HybPiper was designed for targeted sequence capture, in which DNA
    sequencing libraries are enriched for gene regions of interest,
    especially for phylogenetics. HybPiper is a suite of Python scripts
    that wrap and connect bioinformatics tools in order to extract target
    sequences from high-throughput DNA sequencing reads"""

    homepage = "https://github.com/mossmatters/HybPiper"
    url = "https://github.com/mossmatters/HybPiper/archive/v1.2.0.tar.gz"
    git = "https://github.com/mossmatters/HybPiper/HybPiper.git"
    maintainers("snehring")

    license("GPL-3.0-or-later")

    version("2.1.8", sha256="ff358a560d6dbbec4fdac67457451cb4e6ca21b8661044c43902aa013d805e47")
    version("1.3.1", sha256="7ca07a9390d1ca52c72721774fa220546f18d3fa3b58500f68f3b2d89dbc0ecf")
    version("1.2.0", sha256="34c7b324e9bcacb6ccfe87dc50615d6f93866433b61a59291707efa858b6df57")

    build_system(
        conditional("python_pip", when="@2.1:"),
        conditional("generic", when="@:1.3.1"),
        default="python_pip",
    )

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("python@3.9:", type=("build", "run"), when="@2.1:")

    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-biopython@1.80:", type=("build", "run"), when="@2.1:")
    depends_on("py-matplotlib", type=("build", "run"), when="@2.1:")
    depends_on("py-pandas", type=("build", "run"), when="@2.1:")
    depends_on("py-pebble", type=("build", "run"), when="@2.1:")
    depends_on("py-progressbar2", type=("build", "run"), when="@2.1:")
    depends_on("py-psutil", type=("build", "run"), when="@2.1:")
    depends_on("py-scipy", type=("build", "run"), when="@2.1:")
    depends_on("py-seaborn", type=("build", "run"), when="@2.1:")

    depends_on("exonerate")
    depends_on("exonerate@2.4:", when="@2.1:")
    depends_on("bbmap", when="@2.1:")
    depends_on("blast-plus")
    depends_on("blast-plus@2.9.0:", when="@2.1:")
    depends_on("bwa")
    depends_on("diamond", when="@2.1:")
    depends_on("mafft", when="@2.1:")
    depends_on("parallel")
    depends_on("samtools")
    depends_on("samtools@1.14", when="@2.1:")
    depends_on("spades")
    depends_on("spades@3.15.4:", when="@2.1:")

    def setup_run_environment(self, env):
        env.set("HYBPIPER_HOME", self.prefix)

    @when("@:1.3.1")
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("*.py", prefix.bin)
