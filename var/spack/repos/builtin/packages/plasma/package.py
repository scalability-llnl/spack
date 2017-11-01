##############################################################################
# Copyright (c) 2017, Innovative Computing Laboratory
# Produced at the Innovative Computing Laboratory.
#
# Created by Piotr Luszczek, luszczek@icl.utk.edu, All rights reserved.
#
# For details, see https://github.com/llnl/spack
#
##############################################################################
#
from spack import *


class Plasma(MakefilePackage):
    """Parallel Linear Algebra Software for Multicore Architectures, PLASMA is
    a software package for solving problems in dense linear algebra using
    multicore processors and Xeon Phi coprocessors. PLASMA provides
    implementations of state-of-the-art algorithms using cutting-edge task
    scheduling techniques. PLASMA currently offers a collection of routines for
    solving linear systems of equations, least squares problems, eigenvalue
    problems, and singular value problems."""

    homepage = "https://bitbucket.org/icl/plasma/"
    url      = "https://bitbucket.org/icl/plasma/downloads/plasma-17.1.tar.gz"

    version("17.1", "64b410b76023a41b3f07a5f0dca554e1")

    version("develop", hg="https://luszczek@bitbucket.org/icl/plasma")

    depends_on("blas")
    depends_on("lapack")

    conflicts("atlas")  # does not have LAPACKE interface

    # missing LAPACKE features and/or CBLAS headers
    conflicts("netlib-lapack@:3.5.999")

    # clashes with OpenBLAS declarations and has a problem compiling on its own
    conflicts("cblas")

    conflicts("openblas-with-lapack")  # incomplete LAPACK implementation
    conflicts("veclibfort")

    # only GCC 4.9+ and higher have sufficient support for OpenMP 4+ tasks+deps
    conflicts("%gcc@:4.8.99")

    conflicts("%cce")
    conflicts("%clang")
    conflicts("%intel")
    conflicts("%nag")
    conflicts("%pgi")
    conflicts("%xl")
    conflicts("%xl_r")

    patch("remove_absolute_mkl_include.patch", when="@17.1")
    patch("add_netlib_lapacke_detection.patch", when="@17.1")

    def edit(self, spec, prefix):
        # copy "make.inc.mkl-gcc" provided by default into "make.inc"
        open("make.inc", "w").write(open("make.inc.mkl-gcc").read())

        make_inc = FileFilter("make.inc")

        ld_flags = self.spec["lapack"].libs.ld_flags + " " + \
            self.spec["blas"].libs.ld_flags

        if "^mkl" not in spec:
            make_inc.filter("-DPLASMA_WITH_MKL", "")  # not using MKL

        if "^netlib-lapack" in spec:
            ld_flags += " -llapacke -lcblas"

        header_flags = ""
        # accumulate CPP flags for headers: <cblas.h> and <lapacke.h>
        for dep in ("blas", "lapack"):
            try:  # in case the dependency does not provide header flags
                header_flags += " " + spec[dep].headers.cpp_flags
            except:
                pass

        make_inc.filter("CFLAGS +[+]=", "CFLAGS += " + header_flags + " ")

        # pass prefix variable from "make.inc" to "Makefile"
        make_inc.filter("# --*", "prefix={0}".format(self.prefix))

        # make sure CC variable comes from build environment
        make_inc.filter("CC *[?]*= * .*cc", "")

        make_inc.filter("LIBS *[?]*= * .*", "LIBS = " + ld_flags)

    @property
    def build_targets(self):
        targets = list()

        # use $CC set by Spack
        targets.append("CC = {0}".format(self.compiler.cc))

        ld_flags = ""

        if "^mkl" in self.spec:
            targets.append("MKLROOT = {0}".format(env["MKLROOT"]))

        if "^netlib-lapack" in self.spec:
            ld_flags = " -llapacke -lcblas"

        system_libs = find_system_libraries(['libm'])

        # pass LAPACK, BLAS, and libm library flags
        targets.append("LIBS = {0} {1} {2} {3}".format(
            self.spec["lapack"].libs.ld_flags,
            self.spec["blas"].libs.ld_flags, ld_flags, system_libs.ld_flags))

        return targets
