# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xxdiff(MakefilePackage):
    """Graphical File And Directories Comparator And Merge Tool."""

    homepage = "https://furius.ca/xxdiff/"
    git = "https://github.com/blais/xxdiff.git"

    maintainers("vanderwb")

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version("2023-01-10", commit="604300ea9875611726ba885fb14f872b964df579")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("flex@2.5.31:", type="build")
    depends_on("bison", type="build")
    depends_on("qt@5:", type=("build", "link", "run"))

    def edit(self, spec, prefix):
        env["QMAKE"] = "qmake"

    def build(self, spec, prefix):
        with working_dir("src"):
            # Create the makefile
            make("-f", "Makefile.bootstrap")
            make()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("bin/xxdiff", prefix.bin)
