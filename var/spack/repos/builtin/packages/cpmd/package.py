# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cpmd(MakefilePackage):
    """The CPMD code is a parallelized plane wave / pseudopotential
    implementation of Density Functional Theory, particularly
    designed for ab-initio molecular dynamics."""

    homepage = "https://www.cpmd.org/wordpress/"
    url = "https://github.com/CPMD-code/CPMD/archive/refs/tags/4.3.tar.gz"

    license("MIT")

    version("4.3", sha256="e0290f9da0d255f90a612e60662b14a97ca53003f89073c6af84fa7bc8739f65")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("omp", description="Enables the use of OMP instructions", default=False)
    variant("mpi", description="Build with MPI support", default=False)

    depends_on("lapack")
    depends_on("mpi", when="+mpi")

    conflicts("^openblas threads=none", when="+omp")
    conflicts("^openblas threads=pthreads", when="+omp")

    def edit(self, spec, prefix):
        # patch configure file
        cbase = "LINUX-GFORTRAN"
        cp = FileFilter(join_path("configure", cbase))
        # Compilers
        if spec.satisfies("+mpi"):
            fc = spec["mpi"].mpifc
            cc = spec["mpi"].mpicc
        else:
            fc = spack_fc
            cc = spack_cc
            cp.filter(r"FFLAGS='([^']*)'", "FFLAGS='\\1 -fallow-argument-mismatch'")

        cp.filter("FC=.+", "FC='{0}'".format(fc))
        cp.filter("CC=.+", "CC='{0}'".format(cc))
        cp.filter("LD=.+", "LD='{0}'".format(fc))

        # MPI flag
        if spec.satisfies("+mpi"):
            cp.filter("-D__Linux", "-D__Linux -D__PARALLEL")

        # OMP flag
        if spec.satisfies("+omp"):
            cp.filter("-fopenmp", self.compiler.openmp_flag)

        # lapack
        cp.filter("LIBS=.+", "LIBS='{0}'".format(spec["lapack"].libs.ld_flags))

        # LFLAGS
        cp.filter("'-static '", "")

        # Compiler specific
        if spec.satisfies("%fj"):
            cp.filter("-ffixed-form", "-Fixed")
            cp.filter("-ffree-line-length-none", "")
            cp.filter("-falign-commons", "-Kalign_commons")

        # create Makefile
        bash = which("bash")
        if spec.satisfies("+omp"):
            bash("./configure.sh", "-omp", cbase)
        else:
            bash("./configure.sh", cbase)

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def test_cpmd(self):
        """check cpmd.x outputs"""
        test_dir = self.test_suite.current_test_data_dir
        test_file = join_path(test_dir, "1-h2o-pbc-geoopt.inp")
        opts = []
        if self.spec.satisfies("+mpi"):
            exe_name = self.spec["mpi"].prefix.bin.mpirun
            opts.extend(["-n", "2"])
            opts.append(join_path(self.prefix.bin, "cpmd.x"))
        else:
            exe_name = "cpmd.x"
        opts.append(test_file)
        opts.append(test_dir)
        cpmd = which(exe_name)
        out = cpmd(*opts, output=str.split, error=str.split)

        expected = [
            "2       1        H        O              1.84444     0.97604",
            "3       1        H        O              1.84444     0.97604",
            "2   1   3         H     O     H              103.8663",
        ]
        check_outputs(expected, out)
