# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pennant(MakefilePackage):
    """PENNANT is an unstructured mesh physics mini-app designed
    for advanced architecture research. It contains mesh data
    structures and a few physics algorithms adapted
    from the LANL rad-hydro code FLAG, and gives a sample of
    the typical memory access patterns of FLAG.
    """

    homepage = "https://github.com/lanl/PENNANT"
    url = "https://github.com/lanl/PENNANT/archive/pennant_v0.9.tar.gz"
    tags = ["proxy-app"]

    version("0.9", sha256="5fc07e64c246f8b1b552595a0868ba0042b7a2410aa844e7b510bc31e2512dd8")
    version("0.8", sha256="b07226b377c0e22c0f9a631be07ab28793c6d9a337a7a6eed2c7d4dc79f93f18")
    version("0.7", sha256="a6b7e76f7e68a693fd12ec338eaeb59430db9f12b69279b24f78724882684ae4")
    version("0.6", sha256="0b317c19d6af96fe0544afb19ea503449c9f57869b9ad788f654ebec316341f4")
    version("0.5", sha256="21ef5889731fad0075f9dab8ffa97af8fd8ff87f6a5fe6434916b6e28cf64e43")
    version("0.4", sha256="65b81b92ed6fdbe407310948dd76ffb48cca155ee05c1f990a649faf81b45bb0")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI support")
    variant("openmp", default=True, description="Build with OpenMP support")
    variant("debug", default=False, description="Enable debug")

    depends_on("mpi", when="+mpi")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        debug = "-g"
        opt = "-O3"

        if self.compiler.name == "intel":
            opt += " -fast -fno-alias"
        if self.compiler.name == "pgi":
            opt += " -fastsse"

        makefile.filter("CXXFLAGS_DEBUG .*", "CXXFLAGS_DEBUG := {0}".format(debug))
        makefile.filter("CXXFLAGS_OPT .*", "CXXFLAGS_OPT := {0}".format(opt))
        makefile.filter(
            "CXXFLAGS_OPENMP .*", "CXXFLAGS_OPENMP := {0}".format(self.compiler.openmp_flag)
        )

        if "+mpi" in spec:
            makefile.filter("CXX .*", "CXX := {0}".format(spec["mpi"].mpicxx))
        else:
            makefile.filter("-DUSE_MPI", "#")
            makefile.filter("CXX .*", "CXX := c++")

        if "+openmp" not in spec:
            makefile.filter(".*CXXFLAGS_OPENMP.*", "#")

        if "+debug" in spec:
            makefile.filter(".*(CXXFLAGS_OPT).*", "CXXFLAGS := $(CXXFLAGS_DEBUG)")

    def install(self, spec, prefix):
        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        mkdirp(prefix.bin)
        install("build/pennant", prefix.bin)
        install_dir("doc")
        install_dir("test")
        install("LICENSE", prefix)
        install("README", prefix)
