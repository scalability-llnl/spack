# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tcoffee(MakefilePackage):
    """T-Coffee is a multiple sequence alignment program."""

    homepage = "http://www.tcoffee.org/"
    git = "https://github.com/cbcrg/tcoffee.git"

    version("2017-08-17", commit="f389b558e91d0f82e7db934d9a79ce285f853a71")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("perl", type=("build", "run"))
    depends_on("blast-plus")
    depends_on("dialign-tx")
    depends_on("viennarna")
    depends_on("clustalw")
    depends_on("tmalign")
    depends_on("muscle")
    depends_on("mafft")
    depends_on("pcma")
    depends_on("poamsa")
    depends_on("probconsrna")

    build_directory = "compile"

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make("t_coffee")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install("t_coffee", prefix.bin)
