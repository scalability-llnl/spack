# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DhpmmF(MakefilePackage):
    """DHPMM_P:High-precision Matrix Multiplication with Faithful Rounding"""

    homepage = "http://www.math.twcu.ac.jp/ogita/post-k/"
    url = "http://www.math.twcu.ac.jp/ogita/post-k/software/DHPMM_F/DHPMM_F_alpha.tar.gz"

    license("MIT")

    version("alpha", sha256="35321ecbc749f2682775ffcd27833afc8c8eb4fa7753ce769727c9d1fe097848")

    depends_on("blas", type="link")
    depends_on("lapack", type="link")

    def patch(self):
        math_libs = self.spec["lapack"].libs + self.spec["blas"].libs
        makefile = FileFilter("Makefile")
        if self.spec.satisfies("%gcc"):
            makefile.filter(r"^MKL\s+=\s1", "MKL=0")
            makefile.filter(r"^CC\s+=\sgcc", "CC={0}".format(spack_cc))
            makefile.filter(r"^CXX\s+=\sg\+\+", "CXX={0}".format(spack_cxx))
            makefile.filter(
                r"^BLASLIBS\s+=\s-llapack\s-lblas", "BLASLIBS={0}".format(math_libs.ld_flags)
            )
        elif self.spec.satisfies("%fj"):
            makefile.filter(r"^#ENV\s+=\sFX100", "ENV=FX100")
            makefile.filter(r"^ENV\s+=\sGCC", "#ENV=GCC")
            makefile.filter(r"^MKL\s+=\s1", "MKL=0")
            makefile.filter(r"^CC\s+=\sfccpx", "CC={0}".format(spack_cc))
            makefile.filter(r"^CXX\s+=\sFCCpx", "CXX={0}".format(spack_cxx))
            makefile.filter(
                r"^BLASLIBS\s+=\s-llapack\s-lblas", "BLASLIBS={0}".format(math_libs.ld_flags)
            )
        elif self.spec.satisfies("%intel"):
            makefile.filter(r"^ENV\s+=\sGCC", "#ENV=GCC")
            makefile.filter(r"^ENV\s+=\sICC", "ENV=ICC")
            makefile.filter(r"^CC\s+=\sicc", "CC={0}".format(spack_cc))
            makefile.filter(r"^CXX\s+=\sicc", "CXX={0}".format(spack_cxx))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("test/source4_SpMV", prefix.bin)
