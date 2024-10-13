# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import shutil

from spack.build_systems import cmake
from spack.package import *


class Siesta(MakefilePackage, CMakePackage):
    """SIESTA performs electronic structure calculations and ab initio molecular
    dynamics simulations of molecules and solids.
    """

    build_system(
        conditional("cmake", when="@5:"), conditional("makefile", when="@:4"), default="cmake"
    )

    homepage = "https://departments.icmab.es/leem/siesta/"
    git = "https://gitlab.com/siesta-project/siesta"

    version(
        "5.0.1",
        url="https://gitlab.com/siesta-project/siesta/-/archive/5.0.1/siesta-5.0.1.tar.gz",
        sha256="800a22a831c1d36c6f5fe4aa9c49ee510cbd49a0b2f87b3c8bf3edb6ebd0193a",
    )

    version(
        "5.0.0",
        url="https://gitlab.com/siesta-project/siesta/-/archive/rel-5.0/siesta-rel-5.0.tar.gz",
        sha256="0b40c341dfd47e99e7e191189600bbcaadb0f9af03977fefed6a69836bd523e4",
    )
    version(
        "4.1.5",
        url="https://gitlab.com/siesta-project/siesta/-/archive/v4.1.5/siesta-v4.1.5.tar.gz",
        sha256="adc88619bf7e17fca2c67ecdcdae1f07ec4b3caf3541c0edf12964c8c330edc9",
    )

    license("GPL-3.0-or-later")

    version("4.0.2", sha256="bafbda19358f0c1dd39bb1253c92ee548791a1c0f648977051d2657216874f7e")
    version(
        "4.0.1",
        sha256="bfb9e4335ae1d1639a749ce7e679e739fdead5ee5766b5356ea1d259a6b1e6d1",
        url="https://launchpad.net/siesta/4.0/4.0.1/+download/siesta-4.0.1.tar.gz",
    )
    version(
        "3.2-pl-5",
        sha256="e438bb007608e54c650e14de7fa0b5c72562abb09cbd92dcfb5275becd929a23",
        url="http://departments.icmab.es/leem/siesta/CodeAccess/Code/siesta-3.2-pl-5.tgz",
    )

    patch("configure.patch", when="@:4.0")

    variant("mpi", default=True, description="Builds with mpi support")
    variant("openmp", default=True, description="Enables OpenMP support")
    variant("netcdf", default=False, description="Compile with Netcdf")
    variant("metis", default=False, description="Activate Metis as a possible ordering library")
    variant("elpa", default=False, description="Use ELPA")
    variant("mumps", default=False, description="Compile with support for MUMPS solvers")
    variant("pexsi", default=False, description="Compile with PEXSI")
    variant(
        "cray",
        default=False,
        description="Enable specific cray settings for using cray-hdf5"
        " and cray-netcdf modulefiles",
    )
    variant("debug", default=False, description="Build in debug  mode")
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "check"),
    )

    depends_on("mpi", when="+mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack", when="+mpi")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("cray-libsci+openmp", when="^[virtuals=cray-libsci] cray-libsci")
    depends_on("metis@5:", when="+metis")
    depends_on("elpa", when="+elpa")
    depends_on("mumps", when="+mumps")
    depends_on("pexsi", when="+pexsi")

    with when("build_system=cmake"):
        depends_on("cmake@3.20:", type="build")

    def flag_handler(self, name, flags):
        if "%gcc@10:" in self.spec and name == "fflags":
            flags.append("-fallow-argument-mismatch")
        return flags, None, None

    def edit(self, spec, prefix):
        sh = which("sh")
        if "+cray" in spec:
            netcdff_prefix = os.environ.get("NETCDF_DIR", "")
            hdf5_prefix = os.environ.get("HDF5_DIR", "")
        if spec.satisfies("@:4.0.2 +mpi"):
            configure_args = [
                "--enable-mpi",
                "--with-blas=%s" % spec["blas"].libs,
                "--with-lapack=%s" % spec["lapack"].libs,
                # need to include BLAS below because Intel MKL's
                # BLACS depends on BLAS, otherwise the compiler
                # test fails
                "--with-blacs=%s" % (spec["scalapack"].libs + spec["blas"].libs),
                "--with-scalapack=%s" % spec["scalapack"].libs,
                # need to specify MPIFC explicitly below, otherwise
                # Intel's mpiifort is not found
                "MPIFC=%s" % spec["mpi"].mpifc,
            ]
            if "+cray" in spec:
                configure_args += ["--with-netcdf={0}/lib/libnetcdff.so".format(netcdff_prefix)]
            else:
                configure_args += [
                    "--with-netcdf=%s" % (spec["netcdf-fortran"].libs + spec["netcdf-c"].libs)
                ]

            if self.spec.satisfies("%gcc"):
                if "+cray" in spec:
                    configure_args.append(
                        "FCFLAGS=-ffree-line-length-0 -I{0}/include".format(netcdff_prefix)
                    )
                else:
                    configure_args.append("FCFLAGS=-ffree-line-length-0")
            for d in ["Obj", "Obj_trans"]:
                with working_dir(d, create=True):
                    sh("../Src/configure", *configure_args)
                    if spec.satisfies("@:4.0%intel"):
                        with open("arch.make", "a") as f:
                            f.write("\natom.o: atom.F\n")
                            f.write("\t$(FC) -c $(FFLAGS) -O1")
                            f.write("$(INCFLAGS) $(FPPFLAGS) $<")
                    sh("../Src/obj_setup.sh")

        elif self.spec.satisfies("@:4.1.5"):
            with working_dir("Obj", create=True):
                sh("../Src/obj_setup.sh")
                if spec.satisfies("@:4.1.5%gcc"):
                    shutil.copy("./gfortran.make", "./arch.make")
                    libs_arg = []
                    fppflags_arg = []
                    arch_make = FileFilter("./arch.make")
                    arch_make.filter(
                        "FFLAGS = .*",
                        "FFLAGS = {0}".format(
                            "-O2 -fPIC -ftree-vectorize -fallow-argument-mismatch"
                        ),
                    )

                    if "+debug" in spec:
                        arch_make.filter("FFLAGS_DEBUG=.*", "FFLAGS_DEBUG= -g -O1")

                    if "^cray-libsci" in spec:
                        libs_arg.append("-L{0}/lib -lsci_gnu".format(spec["cray-libsci"].prefix))

                    with open("arch.make", "a") as f:
                        if "+mpi" in spec:
                            arch_make.filter("CC = .*", "CC = {0}".format(spec["mpi"].mpicc))
                            arch_make.filter("FC = .*", "FC = {0}".format(spec["mpi"].mpifc))
                            if "^cray-libsci" in spec:
                                libs_arg.append("-lsci_gnu_mpi")
                            f.write("MPI_INTERFACE = libmpi_f90.a\n")
                            f.write("MPI_INCLUDE = .\n")
                            f.write("LIBS += " + spec["scalapack"].libs.ld_flags + "\n")
                            fppflags_arg.append("-DMPI ")

                        if "+openmp" in spec:
                            f.write("FFLAGS += -fopenmp\n")
                            f.write("LIBS += -fopenmp\n")

                        if "+netcdf" in spec:
                            if "+cray" in spec:
                                libs_arg.append(
                                    "-L{0}/lib -lnetcdff -lnetcdf".format(netcdff_prefix)
                                )
                                libs_arg.append(
                                    "-L{0}/lib -lhdf5_fortran -lhdf5".format(hdf5_prefix)
                                )
                            else:
                                libs_arg.append(
                                    "-L{0}/lib -lnetcdff -lnetcdf".format(
                                        spec["netcdf-fortran"].prefix
                                    )
                                )
                                libs_arg.append(
                                    "-L{0}/lib -lhdf5_fortran -lhdf5".format(spec["hdf5"].prefix)
                                )

                        if "+metis" in spec:
                            libs_arg.append("-L{0} -lmetis".format(self.spec["metis"].prefix.lib))
                            fppflags_arg.append("-DSIESTA__METIS ")

                        if "elpa" in spec:
                            elpa = spec["elpa"]
                            elpa_suffix = "_openmp" if "+openmp" in elpa else ""
                            elpa_incdir = elpa.headers.directories[0]
                            libs_arg.append(
                                "-L{0} -lelpa{1}".format(self.spec["elpa"].prefix.lib, elpa_suffix)
                            )
                            fppflags_arg.append(
                                "-DSIESTA__ELPA  -I{0}".format(join_path(elpa_incdir, "modules"))
                            )

                        if "mumps" in spec:
                            libs_arg.append(
                                "-L{0} -lmumps_common -lzmumps".format(
                                    self.spec["mumps"].prefix.lib
                                )
                            )
                            fppflags_arg.append("-DSIESTA__MUMPS ")

                        if "+pexsi" in spec:
                            libs_arg.append(
                                "-L{0} -lpexsi_linux".format(self.spec["pexsi"].prefix.lib)
                            )
                            fppflags_arg.append("-DSIESTA__PEXSI ")
                            f.write("INCFLAGS += -I{0}/include".format(self.spec["pexsi"].prefix))

                        arch_make.filter("^LIBS =.*", "LIBS = {0}".format(" ".join(libs_arg)))
                        f.write("FPPFLAGS = {0}".format(" ".join(fppflags_arg)))

    def build(self, spec, prefix):
        with working_dir("Obj"):
            make(parallel=False)
        if spec.satisfies("@:4.0.2"):
            with working_dir("Obj_trans"):
                make("transiesta", parallel=False)
            with working_dir("Util"):
                sh = which("sh")
                sh("build_all.sh")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        with working_dir("Obj"):
            install("siesta", prefix.bin)
        if spec.satisfies("@:4.0.2"):
            with working_dir("Obj_trans"):
                install("transiesta", prefix.bin)
        for root, _, files in os.walk("Util"):
            for fname in files:
                fname = join_path(root, fname)
                if os.access(fname, os.X_OK):
                    install(fname, prefix.bin)


class CMakeBuilder(cmake.CMakeBuilder):
    """Use the new CMake build system to build siesta@5.0.0:."""

    def cmake_args(self):
        spec = self.spec
        args = []

        args += ["-DBLAS_LIBRARIES={0}".format(self.spec["blas"].libs.link_flags)]
        args += ["-DLAPACK_LIBRARIES={0}".format(self.spec["lapack"].libs.link_flags)]

        if "+mpi" in spec:
            args += [
                "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
                "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
                "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
            ]
            args += ["-DSIESTA_WITH_MPI=ON"]
            args += ["-DSCALAPACK_LIBRARY={0}".format(spec["scalapack"].libs.joined(";"))]

        if "+openmp" in spec:
            args += ["-DSIESTA_WITH_OPENMP=ON"]
            if "+cray" in spec:
                args += ["-DFortran_FLAGS=-fopenmp"]

        if "build_type=Debug" in spec:
            args += [
                "-DFortran_FLAGS=-Og -g -Wall -fcheck=all -fbacktrace"
                " -Warray-bounds -Wunused -Wuninitialized"
            ]
        else:
            args += ["-DFortran_FLAGS=-O2 -fPIC -ftree-vectorize  -fallow-argument-mismatch"]

        if "+netcdf" in spec:
            args += ["-DSIESTA_WITH_NETCDF=ON"]
            if "+cray" in spec:
                args += ["-DNetCDF_PATH={0}".format(os.environ.get("NETCDF_DIR", ""))]
            else:
                args += ["-DNetCDF_PATH={0}".format(spec["netcdf-fortran"].prefix)]

        if "+elpa" in spec:
            args += ["-DSIESTA_WITH_ELPA=ON"]

        if "+mumps" in spec:
            args += ["-DSIESTA__MUMPS=ON"]
            args += [
                "-DSIESTA_LINKER_FLAGS=-L{0} -lmumps_common -lzmumps".format(
                    self.spec["mumps"].prefix.lib
                )
            ]

        if "+metis" in spec:
            args += ["-DSIESTA__METIS=ON"]
            args += ["-DSIESTA_LINKER_FLAGS=-L{0} -lmetis".format(self.spec["metis"].prefix.lib)]

        return args
