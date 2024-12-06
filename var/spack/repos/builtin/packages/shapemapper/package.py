# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shapemapper(CMakePackage):
    """
    ShapeMapper automates the calculation of RNA structure probing reactivities from mutational
    profiling (MaP) experiments, in which chemical adducts on RNA are detected as internal
    mutations in cDNA through reverse transcription and read out by massively parallel sequencing.
    """

    homepage = "https://github.com/Weeks-UNC/shapemapper2"
    url = "https://github.com/Weeks-UNC/shapemapper2/releases/download/2.1.5/shapemapper-2.1.5-source-only.tar.gz"

    maintainers("snehring")

    license("MIT")

    version(
        "2.2.0",
        sha256="eec1bfca339731816142bf2e7826dfb2e125588d72a1f7c36aaa927393e6fbec",
        url="https://github.com/Weeks-UNC/shapemapper2/releases/download/2.2.0/shapemapper2-2.2-source-only.tar.gz",
    )
    version(
        "2.1.5",
        sha256="0846a5d8b5f01d2d039fad4b957df0b6220a8505463f1a410368a1b90d2b227c",
        url="https://github.com/Weeks-UNC/shapemapper2/releases/download/2.1.5/shapemapper-2.1.5-source-only.tar.gz",
    )

    depends_on("cxx", type="build")  # generated

    depends_on("bowtie2@2.3.0:", type="run", when="@2.1.5")
    depends_on("bowtie2@2.3.4:", type="run", when="@2.2.0:")
    depends_on("perl+threads", type="run")
    depends_on("pv@1.6.20:", type="run")
    # hard version dep due to jni
    depends_on("bbmap@37.78", type="run")
    depends_on("boost+filesystem+program_options+iostreams+system")
    depends_on("star@2.5.2:", type="run")
    depends_on("pv@1.6.0:", type="run")
    depends_on("python@3.7:", type="run", when="@2.1.5")
    depends_on("python@3.9.12:", type="run", when="@2.2.0")
    depends_on("graphviz@2.38.0:", type="run", when="@2.1.5")
    depends_on("graphviz@7.1.0:", type="run", when="@2.2.0:")
    depends_on("py-numpy@1.19.5:1.19", type="run", when="@2.2.0:")
    depends_on("py-scikit-learn@0.18.1:", type="run", when="@2.1.5")
    depends_on("py-scikit-learn@1.1.2:", type="run", when="@2.2.0:")
    depends_on("py-matplotlib@1.5.1:3.3", type="run", when="@2.1.5")
    depends_on("py-matplotlib@3.6.2:3.6", type="run", when="@2.2.0:")
    depends_on("zlib-api")

    build_directory = "build"

    def install(self, spec, prefix):
        for d in ["docs", "internals", "util"]:
            mkdirp(join_path(prefix, d))
            install_tree(d, join_path(prefix, d))
        for f in ["shapemapper", "README.md"]:
            install(f, prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
