# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import shutil

from spack.package import *


class SiestaRelmax3(MakefilePackage):
    """The MaX3 branch of the SIESTA program is a special branch
    that contains all the features currently implemented within
    the MaX Center of Excellence EU H2020 project.
    This branch is intended for HPC users who want to try
    the new optimizations and enhancements, and provide feedback on them.
    """

    homepage = "https://departments.icmab.es/leem/siesta/"
    git = "https://gitlab.com/siesta-project/siesta"

    version(
        "rel-MaX-3",
        sha256="353c73ca8701eeaebca0dfc0790778ffb2095386ea079f3567f7b3ca35aaa8ee",
        url="https://gitlab.com/siesta-project/siesta/-/archive/rel-MaX-3/siesta-rel-MaX-3.tar.gz",
    )

    # Fix dbscr and libgridxc link error and add missing object files
    patch("fix_linkerror.patch")

    # Fix ncdf_parallel link error when using Fujitsu compiler
    patch("fj_fix_use_netcdf_parallel.patch", when="%fj")

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")

    depends_on("hdf5")
    depends_on("elsi@2.6.2")
    depends_on("xmlf90")
    depends_on("libpsml")
    depends_on("libxc")
    depends_on("libgridxc@1.1.0+mpi")
    depends_on("flook")
    depends_on("fftw")
    # use dbcsr and omm-bundle specified in ExtLibs directory
    depends_on("dbcsr@46cd0928465ee6bf21d82e5aac0a1970dcb54501")
    depends_on("omm-bundle@0f863b217889486df299099fed14abb8e7910d56")

    def flag_handler(self, name, flags):
        if "%gcc@10:" in self.spec and name == "fflags":
            flags.append("-fallow-argument-mismatch")
        return flags, None, None

    def edit(self, spec, prefix):
        sh = which("sh")
        with working_dir("Obj", create=True):
            sh("../Src/obj_setup.sh")

            # setup arch.make(compilers and flags)
            shutil.copy("../Config/mk-build/sample-arch-makes/gcc-modules.mk", "./arch.make")
            arch_make = FileFilter("./arch.make")
            arch_make.filter("FC_PARALLEL=.*", "FC_PARALLEL={0}".format(spec["mpi"].mpifc))
            arch_make.filter("FC_SERIAL=.*", "FC_SERIAL={0}".format(spack_fc))
            if spec.satisfies("%fj"):
                arch_make.filter("FFLAGS=.*", "FFLAGS= -Kfast --Nlst -Cpp -X08")
                arch_make.filter("FFLAGS_DEBUG=.*", "FFLAGS_DEBUG= -g -O0 -fPIC -Nlst -Cpp -X08")
                arch_make.filter("RANLIB=echo", "RANLIB=echo\nLDFLAGS= -Kparallel -Kopenmp")

            # setup build.mk
            build_mk = FileFilter("./build.mk")
            build_mk.filter("#XMLF90_ROOT=.*", "XMLF90_ROOT={0}".format(spec["xmlf90"].prefix))
            build_mk.filter("#PSML_ROOT=.*", "PSML_ROOT={0}".format(spec["libpsml"].prefix))
            build_mk.filter("#GRIDXC_ROOT=.*", "GRIDXC_ROOT={0}".format(spec["libgridxc"].prefix))
            build_mk.filter("#ELPA_ROOT=.*", "ELPA_ROOT={0}".format(spec["elsi"].prefix))
            build_mk.filter(
                "#ELPA_INCLUDE_DIRECTORY=.*",
                "ELPA_INCLUDE_DIRECTORY={0}".format(spec["elsi"].prefix.include),
            )
            build_mk.filter("#FLOOK_ROOT=.*", "FLOOK_ROOT={0}".format(spec["flook"].prefix))
            build_mk.filter("#DBCSR_ROOT=.*", "DBCSR_ROOT={0}".format(spec["dbcsr"].prefix))
            build_mk.filter(
                "#OMM_SPARSE_BUNDLE_ROOT=.*",
                "OMM_SPARSE_BUNDLE_ROOT={0}".format(spec["omm-bundle"].prefix),
            )
            build_mk.filter("#NETCDF_ROOT=.*", "NETCDF_ROOT={0}".format(spec["netcdf-c"].prefix))
            build_mk.filter(
                "#NETCDF_LIBS=.*",
                "NETCDF_LIBS= -L{0} -L{1} -L{2} -lnetcdff -lnetcdf  -lhdf5_hl -lhdf5".format(
                    spec["netcdf-c"].prefix.lib,
                    spec["netcdf-fortran"].prefix.lib,
                    spec["hdf5"].prefix.lib,
                ),
            )
            build_mk.filter(
                "#NETCDF_INCFLAGS=.*",
                "NETCDF_INCFLAGS=-I{0} -I{1}".format(
                    spec["netcdf-c"].prefix.include, spec["netcdf-fortran"].prefix.include
                ),
            )
            build_mk.filter(
                "#SCALAPACK_LIBS=.*", "SCALAPACK_LIBS={0}".format(spec["scalapack"].libs)
            )
            build_mk.filter(
                "#LAPACK_LIBS=.*",
                "LAPACK_LIBS={0} {1}".format(spec["lapack"].libs, spec["blas"].libs),
            )

    def build(self, spec, prefix):
        with working_dir("Obj"):
            make()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        with working_dir("Obj"):
            install("siesta", prefix.bin)
