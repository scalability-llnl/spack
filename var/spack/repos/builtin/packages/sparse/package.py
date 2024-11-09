# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sparse(MakefilePackage):
    """An open source sparse linear equation solver."""

    homepage = "https://sparse.sourceforge.net/"
    url = "https://downloads.sourceforge.net/project/sparse/sparse/sparse1.4b/sparse1.4b.tar.gz"

    maintainers("wortiz")

    license("MIT")

    version("1.4b", sha256="63e6646244fd8f4d89f7f70fbf4cfd46b7688d21b22840a0ce57d294a7496d28")

    depends_on("c", type="build")  # generated

    variant("pic", default=True, description="Build with position independent code")

    def edit(self, spec, prefix):
        with working_dir("./src"):
            makefile = FileFilter("Makefile")
            if "+pic" in self.spec:
                makefile.filter(
                    "CFLAGS = .*", "CFLAGS = -O2 {0}".format(self.compiler.cc_pic_flag)
                )
            else:
                makefile.filter("CFLAGS = .*", "CFLAGS = -O2")
            makefile.filter("CC = .*", "CC = {0}".format(spack_cc))
            makefile.filter("LIBRARY = .*", "LIBRARY = ../lib/libsparse.a")

    def build(self, spec, prefix):
        with working_dir("./src"):
            make()

    def install(self, spec, prefix):
        mkdir(prefix.include)
        install_tree("lib", prefix.lib)
        install_tree("bin", prefix.bin)
        install("src/*.h", prefix.include)
