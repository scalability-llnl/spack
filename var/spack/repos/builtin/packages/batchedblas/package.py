# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Batchedblas(MakefilePackage):
    """Batched BLAS is one of the new approaches for a task-based BLAS
    invocation, and it is defined as a new interface that allows users to
    execute multiple independent BLAS operations as a single subroutine call"""

    homepage = "https://www.r-ccs.riken.jp/labs/lpnctrt/projects/batchedblas/index.html"
    url = "https://www.r-ccs.riken.jp/labs/lpnctrt/projects/batchedblas/BatchedBLAS-1.0.tar.gz"

    license("BSD-2-Clause")

    version("1.0", sha256="798ae4e7cc4ad5c3d5f3479f3d001da566d7d5205779103aaf10cd5b956ba433")

    depends_on("c", type="build")  # generated

    depends_on("blas")

    patch("AVX2.patch")

    def edit(self, spec, prefix):
        CCFLAGS = [self.compiler.openmp_flag, "-I./", "-O3"]
        BLAS = ["-lm", spec["blas"].libs.ld_flags]
        if spec["blas"].name not in INTEL_MATH_LIBRARIES:
            CCFLAGS.append("-D_CBLAS_")
        if spec.satisfies("%intel"):
            CCFLAGS.extend(["-Os"])
        elif spec.satisfies("%fj"):
            CCFLAGS.extend(["-std=gnu11", "-Kfast,ocl", "-Nclang"])
        makefile_src = FileFilter("bblas_src/Makefile")
        makefile_src.filter(r"^\s*CCFLAG\s*=.*", "CCFLAG = %s" % " ".join(CCFLAGS))
        makefile_src.filter(r"^\s*BLAS\s*=.*", "BLAS = %s" % " ".join(BLAS))

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        install(join_path("bblas_src", "*.h"), prefix.include)
        install(join_path("bblas_src", "libbblas.a"), prefix.lib)
        install(join_path("bblas_src", "libbblas.so"), prefix.lib)
