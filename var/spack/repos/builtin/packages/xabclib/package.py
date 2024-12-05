# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xabclib(MakefilePackage):
    """
    Xabclib (eXtended ABCLib) is a numerical library with auto-tuning facility.
    """

    homepage = "http://www.abc-lib.org/Xabclib/index.html"
    url = "http://www.abc-lib.org/Xabclib/Release/Xabclib-v1.03.tar.gz"

    version("1.03", sha256="9d200f40f1db87abc26cfe75a22db3a6d972988a28fc0ce8421a0c88cc574d1a")

    def edit(self, spec, prefix):
        cc = [spack_cc, "-O3", self.compiler.openmp_flag]
        fc = [spack_fc, "-O3", self.compiler.openmp_flag]
        if spec.satisfies("%gcc"):
            fc.extend(["-ffixed-form", "-cpp"])
        elif spec.satisfies("%fj"):
            fc.extend(["-Fixed", "-Cpp"])
        filter_file("^rm libOpenAT.a$", "rm -f libOpenAT.a", "make.all")
        for makefile in find(".", "makefile", recursive=True):
            m = FileFilter(makefile)
            m.filter("F90 += .*$", "F90 = {0}".format(" ".join(fc)))
            m.filter("F90O3 += .*$", "F90O3 = {0}".format(" ".join(fc)))
            m.filter("CC += .*$", "CC = {0}".format(" ".join(cc)))
            m.filter("LD += .*$", "LD = {0}".format(" ".join(fc)))
            if spec.satisfies("%fj") and "samples_c" in makefile:
                m.filter("$(LD)", "$(LD) -mlcmain=main", string=True)

    def build(self, spec, prefix):
        sh = which("sh")
        sh("./make.all")

    def install(self, spec, prefix):
        mkdir(prefix.lib)
        mkdir(prefix.doc)
        install("libOpenAT.a", prefix.lib)
        install("Readme.pdf", prefix.doc)

    @property
    def libs(self):
        return find_libraries("libOpenAT", self.prefix.lib, shared=False)
