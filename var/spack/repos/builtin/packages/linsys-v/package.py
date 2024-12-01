# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class LinsysV(MakefilePackage):
    """LINSYS_V: Verified Solution of Linear Systems"""

    homepage = "http://www.math.twcu.ac.jp/ogita/post-k/"
    url = "http://www.math.twcu.ac.jp/ogita/post-k/software/LINSYS_V/LINSYS_V_alpha.tar.gz"

    version("alpha", sha256="6666bc837bb6598b7cdefb233d3d0f2c308a24fe3465e4fe9b6c9762810bb320")

    depends_on("mpi")
    depends_on("blas", type="link")
    depends_on("lapack", type="link")
    depends_on("scalapack", type="link")

    def patch(self):
        math_libs = self.spec["lapack"].libs + self.spec["blas"].libs + self.spec["scalapack"].libs
        makefile = FileFilter("Makefile")
        if self.spec.satisfies("%gcc"):
            makefile.filter(r"^ENV\s+=\sK", "#ENV=K")
            makefile.filter(r"^#ENV\s+=\sGCC", "ENV=GCC")
            makefile.filter(r"^MKL\s+=\s1", "MKL=0")
            makefile.filter(r"^CC\s+=\smpicc", "CC={0}".format(self.spec["mpi"].mpicc))
            makefile.filter(
                r"^LIBS\s+=\s-lscalapack\s-lblacs\s-llapack\s-lblas",
                "LIBS={0}".format(math_libs.ld_flags) + " -lm",
            )
        elif self.spec.satisfies("%fj"):
            makefile.filter(r"^#ENV\s+=\sK", "ENV=K")
            makefile.filter(r"^ENV\s+=\sGCC", "#ENV=GCC")
            makefile.filter(r"^MKL\s+=\s1", "MKL=0")
            makefile.filter(r"^CC\s+=\smpifccpx", "CC={0}".format(self.spec["mpi"].mpicc))
            makefile.filter(
                r"^CFLAGS\s+=\s-Kfast,openmp",
                "CFLAGS=-Ofast -fstrict-aliasing {0}".format(self.compiler.openmp_flag),
            )
            makefile.filter(
                r"^LIBS\s+=\s-SCALAPACK\s-SSL2BLAMP",
                "LIBS=-SSL2BLAMP {0}".format(math_libs.ld_flags),
            )
        elif self.spec.satisfies("%intel"):
            makefile.filter(r"^ENV\s+=\sGCC", "#ENV=GCC")
            makefile.filter(r"^ENV\s+=\sICC", "ENV=ICC")
            makefile.filter(r"^C\s+=\smpiicc", "CC={0}".format(self.spec["mpi"].mpicc))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("ex_linsys_v", prefix.bin)
