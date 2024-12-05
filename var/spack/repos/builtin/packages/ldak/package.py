# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ldak(Package):
    """LDAK is a software package for analyzing GWAS data"""

    homepage = "https://dougspeed.com/ldak/"
    url = "https://dougspeed.com/wp-content/uploads/source.zip"

    maintainers("snehring")

    license("GPL-3.0-only")

    version("5.2", sha256="ba3de4eb4f2d664b3c2a54bef2eb66d1a498ac423179e97a5795d010161b1805")
    version(
        "5.1",
        sha256="ae3eb8c2ef31af210e138336fd6edcd0e3a26ea9bae89fd6c0c6ea33e3a1517e",
        deprecated=True,
    )

    variant("glpk", default=False, description="Use glpk instead of vendored qsopt")

    depends_on("zlib-api")
    depends_on("blas")
    depends_on("lapack")
    depends_on("openblas threads=openmp", when="^[virtuals=blas] openblas")
    depends_on("intel-mkl threads=openmp", when="^[virtuals=blas] intel-mkl")
    depends_on("intel-oneapi-mkl threads=openmp", when="^[virtuals=blas] intel-oneapi-mkl")
    depends_on("glpk", when="+glpk")

    requires("target=x86_64:", when="~glpk", msg="bundled qsopt is only for x86_64")
    requires(
        "^openblas",
        *[f"^{intel_pkg}" for intel_pkg in INTEL_MATH_LIBRARIES],
        policy="one_of",
        msg="Only mkl or openblas are supported for blas/lapack with ldak",
    )

    phases = ["build", "install"]

    def build(self, spec, prefix):
        libs = [
            "-lm",
            (self.spec["lapack"].libs + self.spec["blas"].libs).link_flags,
            self.spec["zlib-api"].libs.link_flags,
        ]
        includes = [
            (self.spec["lapack"].headers + self.spec["blas"].headers).include_flags,
            self.spec["zlib-api"].headers.include_flags,
        ]

        if self.spec.satisfies("~glpk"):
            if self.spec.satisfies("platform=darwin"):
                libs.append("libqsopt.mac.a")
            else:
                libs.append("libqsopt.linux.a")
        else:
            includes.append(self.spec["glpk"].headers.include_flags)
            libs.append(self.spec["glpk"].libs.link_flags)
        if self.spec.satisfies("^mkl"):
            filter_file("#define MKL.*", "#define MKL 1", "ldak.c")
        if self.spec.satisfies("^openblas"):
            filter_file("#define MKL.*", "#define MKL 2", "ldak.c")
            filter_file("#if MKL==2", "#if MKL==2\n#include <cblas.h>\n", "ldak.c")
        if self.spec.satisfies("+glpk"):
            filter_file("#define MET.*", "#define MET 1", "ldak.c")
            filter_file('#include"glpk.h"', "#include<glpk.h>", "ldak.c")
            filter_file(r"weights\[", "tally3[", "weightfuns.c")
        cc = Executable(spack_cc)
        args = ["ldak.c", self.compiler.openmp_flag, "-o", "ldak"] + includes + libs
        cc(*args)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("ldak", prefix.bin.ldak)
