# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re

from spack.build_environment import optimization_flags
from spack.package import *


class Hpcc(MakefilePackage):
    """HPC Challenge is a benchmark suite that measures a range memory access
    patterns.
    The HPC Challenge benchmark consists of basically 7 tests:
        1) HPL - the Linpack TPP benchmark which measures the floating point
           rate of execution for solving a linear system of equations.
        2) DGEMM - measures the floating point rate of execution of double
           precision real matrix-matrix multiplication.
        3) STREAM - a simple synthetic benchmark program that measures
           sustainable memory bandwidth (in GB/s) and
           the corresponding computation rate for simple vector kernel.
        4) PTRANS (parallel matrix transpose) - exercises the communications
           where pairs of processors communicate
           with each other simultaneously. It is a useful test of the total
           communications capacity of the network.
        5) RandomAccess - measures the rate of integer random updates of memory
           (GUPS).
        6) FFT - measures the floating point rate of execution of double
           precision complex one-dimensional Discrete Fourier Transform (DFT).
        7) Communication bandwidth and latency - a set of tests to measure
           latency and bandwidth of  a number of simultaneous communication
           patterns; based on b_eff (effective bandwidth benchmark)."""

    homepage = "https://icl.cs.utk.edu/hpcc"
    url = "https://icl.cs.utk.edu/projectsfiles/hpcc/download/hpcc-1.5.0.tar.gz"
    git = "https://github.com/icl-utk-edu/hpcc.git"

    version("develop", branch="main")
    version("1.5.0", sha256="0a6fef7ab9f3347e549fed65ebb98234feea9ee18aea0c8f59baefbe3cf7ffb8")

    depends_on("c", type="build")  # generated

    variant(
        "fft",
        default="internal",
        description="FFT library to use",
        values=("internal", "fftw2", "mkl"),
        multi=False,
    )

    depends_on("gmake", type="build")
    depends_on("mpi@1.1:")
    depends_on("blas")
    depends_on("fftw@2+mpi", when="fft=fftw2")
    depends_on("mkl", when="fft=mkl")

    arch = f"{platform.system()}-{platform.processor()}"

    config = {
        "@SHELL@": "/bin/sh",
        "@CD@": "cd",
        "@CP@": "cp",
        "@LN_S@": "ln -s",
        "@MKDIR@": "mkdir",
        "@RM@": "/bin/rm -f",
        "@TOUCH@": "touch",
        "@ARCHIVER@": "ar",
        "@ARFLAGS@": "r",
        "@RANLIB@": "echo",
        "@ARCH@": arch,
        "@MPDIR@": "",
        "@MPINC@": "",
        "@MPLIB@": "",
        "@F2CDEFS@": "-DAdd_ -DF77_INTEGER=int -DStringSunStyle",
        "@LADIR@": "",
        "@LAINC@": "",
        "@LALIB@": "",
        "@CC@": None,
        "@CCNOOPT@": "",
        "@CCFLAGS@": "-O3",
        "@LINKER@": "$(CC)",
        "@LINKFLAGS@": "",
    }

    def patch(self):
        if self.spec.satisfies("^fftw"):
            # spack's fftw2 prefix headers with floating point type
            filter_file(r"^\s*#include <fftw.h>", "#include <sfftw.h>", "FFT/wrapfftw.h")
            filter_file(
                r"^\s*#include <fftw_mpi.h>", "#include <sfftw_mpi.h>", "FFT/wrapmpifftw.h"
            )

    def _write_make_arch(self, spec, prefix):
        """write make.arch file"""
        with working_dir("hpl"):
            # copy template make.arch file
            make_arch_filename = f"Make.{self.arch}"
            copy(join_path("setup", "Make.UNKNOWN.in"), make_arch_filename)

            # fill template with values
            make_arch = FileFilter(make_arch_filename)
            for k, v in self.config.items():
                make_arch.filter(k, v)

    def edit(self, spec, prefix):
        # Message Passing library (MPI)
        self.config["@MPINC@"] = spec["mpi"].headers.include_flags
        self.config["@MPLIB@"] = spec["mpi"].libs.search_flags

        lin_alg_libs = []
        # FFT
        if self.spec.variants["fft"].value in ("fftw2", "mkl"):
            self.config["@LAINC@"] += " -DUSING_FFTW"

            if self.spec.variants["fft"].value == "fftw2":
                self.config["@LAINC@"] += spec["fftw-api"].headers.include_flags
                # fftw does not set up libs for version 2
                lin_alg_libs.append(join_path(spec["fftw-api"].prefix.lib, "libsfftw_mpi.so"))
                lin_alg_libs.append(join_path(spec["fftw-api"].prefix.lib, "libsfftw.so"))

            elif (
                self.spec.variants["fft"].value == "mkl"
                and spec["fftw-api"].name in INTEL_MATH_LIBRARIES
            ):
                mklroot = env["MKLROOT"]
                self.config["@LAINC@"] += f" -I{join_path(mklroot, 'include/fftw')}"
                libfftw2x_cdft = join_path(
                    mklroot, "lib", "intel64", "libfftw2x_cdft_DOUBLE_ilp64.a"
                )
                libfftw2xc = join_path(mklroot, "lib", "intel64", "libfftw2xc_double_intel.a")
                if not (os.path.exists(libfftw2x_cdft) and os.path.exists(libfftw2xc)):
                    raise InstallError(
                        "HPCC need fftw2 interface, "
                        "here are brief notes how to make one:\n"
                        "# make fftw2x_cdft interface to mkl\n"
                        "cd $MKLROOT/interfaces/fftw2x_cdft\n"
                        "make libintel64 PRECISION=MKL_DOUBLE "
                        "interface=ilp64 MKLROOT=$MKLROOT\n"
                        "\n"
                        "# make FFTW C wrapper library\n"
                        "cd $MKLROOT/interfaces/fftw2xc\n"
                        "make libintel64 PRECISION=MKL_DOUBLE "
                        "MKLROOT=$MKLROOT\n"
                    )
                lin_alg_libs.append(libfftw2xc)
                lin_alg_libs.append(libfftw2x_cdft)

        # Linear Algebra library (BLAS or VSIPL)
        self.config["@LAINC@"] = spec["blas"].headers.include_flags
        lin_alg_libs = lin_alg_libs + [lib for lib in spec["blas"].libs if lib not in lin_alg_libs]

        # pack all LA/FFT libraries
        self.config["@LALIB@"] = " ".join(lin_alg_libs)

        # Compilers / linkers - Optimization flags
        self.config["@CC@"] = f"{spec['mpi'].mpicc}"

        # Compiler flags for CPU architecture optimizations
        if spec.satisfies("%intel"):
            # with intel-parallel-studio+mpi the '-march' arguments
            # are not passed to icc
            arch_opt = optimization_flags(self.compiler, spec.target)
            self.config["@CCFLAGS@"] = f"-O3 -restrict -ansi-alias -ip {arch_opt}"
            self.config["@CCNOOPT@"] = "-restrict"
        self._write_make_arch(spec, prefix)

    def build(self, spec, prefix):
        make(f"arch={self.arch}")

    def check(self):
        """Simple check that compiled binary is working:
        launch with 4 MPI processes and check that test finished."""
        # copy input
        copy("_hpccinf.txt", "hpccinf.txt")
        # run test
        run = Executable(join_path(os.path.dirname(self.spec["mpi"].mpicc), "mpirun"))
        run("-np", "4", "./hpcc")
        # check output
        hpccoutf = open("hpccoutf.txt", "rt").read()
        if not re.search("End of HPC Challenge tests", hpccoutf):
            raise Exception("Test run was not successfull!")

    def installcheck(self):
        """Same as check but within prefix location"""
        with working_dir(self.prefix.share.hpcc):
            # run test
            run = Executable(join_path(os.path.dirname(self.spec["mpi"].mpicc), "mpirun"))
            run("-np", "4", self.prefix.bin.hpcc)
            # check output
            hpccoutf = open("hpccoutf.txt", "rt").read()
            if not re.search("End of HPC Challenge tests", hpccoutf):
                raise Exception("Test run was not successfull!")

    def install(self, spec, prefix):
        # copy executable
        mkdirp(self.prefix.bin)
        install("hpcc", prefix.bin)
        # copy input example
        mkdirp(self.prefix.share.hpcc)
        install("_hpccinf.txt", join_path(self.prefix.share.hpcc, "hpccinf.txt"))
        # copy documentation
        mkdirp(self.prefix.doc.hpcc)
        install("README.html", self.prefix.doc.hpcc)
        install("README.txt", self.prefix.doc.hpcc)

    def flag_handler(self, name, flags):
        # old GCC defaults to -std=c90 but C99 is required for "restrict"
        if self.spec.satisfies("%gcc@:5.1") and name == "cflags":
            flags.append(self.compiler.c99_flag)
        return (flags, None, None)
