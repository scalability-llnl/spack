# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exciting(MakefilePackage):
    """
    exciting is a full-potential all-electron density-functional-theory package
    implementing the families of linearized augmented planewave methods. It can
    be applied to all kinds of materials, irrespective of the atomic species in
    volved, and also allows for exploring the physics of core electrons. A
    particular focus are excited states within many-body perturbation theory.
    """

    homepage = "https://exciting-code.org/"
    url = "https://exciting.wdfiles.com/local--files/nitrogen-14/exciting.nitrogen-14.tar.gz"
    git = "https://github.com/exciting/exciting.git"

    license("LGPL-2.1-or-later")

    version("oxygen", branch="oxygen_release", preferred=True)
    version("14", sha256="a7feaffdc23881d6c0737d2f79f94d9bf073e85ea358a57196d7f7618a0a3eff")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # as-of-yet unpublished fix to version 14
    patch("dfgather.patch", when="@14", working_dir="src/src_xs", level=0)
    # Patch to add aarch64 in config.guess
    patch("for_aarch64.patch", when="target=aarch64:")

    variant("mpi", default=False, description="Use MPI")
    variant("mkl", default=False, description="Use MKL")
    variant("omp", default=True, description="Use OpenMP")
    variant("scalapack", default=False, description="Use ScaLAPACK")
    depends_on("blas")
    depends_on("lapack")
    depends_on("fftw", when="~mkl")
    depends_on("mkl", when="+mkl")
    depends_on("mpi", when="+mpi")
    depends_on("scalapack", when="+scalapack")
    # conflicts('%gcc@10:', msg='exciting cannot be built with GCC 10')

    requires("%intel", when="^mkl", msg="Intel MKL only works with the Intel compiler")
    requires("%intel", when="^intel-mkl", msg="Intel MKL only works with the Intel compiler")
    requires("%intel", when="^intel-mpi", msg="Intel MPI only works with the Intel compiler")

    def patch(self):
        """Fix bad logic in m_makespectrum.f90 for the Oxygen release"""
        if self.spec.satisfies("@oxygen"):
            filter_file(
                " ".join(
                    ["if ((.not. input%xs%BSE%coupling) .and.", "input%xs%BSE%chibar0) then"]
                ),
                " ".join(
                    [
                        "if ((.not. input%xs%BSE%coupling)",
                        ".and. (.not. input%xs%BSE%chibar0)) then",
                    ]
                ),
                "src/src_xs/m_makespectrum.f90",
                string=True,
            )

    def edit(self, spec, prefix):
        opts = {}
        opts["FCCPP"] = "cpp"
        opts["F90_OPTS"] = "-O3"
        opts["F77_OPTS"] = "-O3"
        opts["CPP_ON_OPTS"] = "-cpp -DXS -DISO -DLIBXC"
        opts["LIB_ARP"] = "libarpack.a"
        opts["F90"] = spack_fc
        opts["F77"] = spack_f77
        if spec.satisfies("+omp"):
            opts["SMPF90_OPTS"] = self.compiler.openmp_flag + " -DUSEOMP"
            opts["SMPF77_OPTS"] = self.compiler.openmp_flag + " -DUSEOMP"
        else:
            opts["BUILDSMP"] = "false"

        if spec.satisfies("%intel"):
            opts["F90_OPTS"] += " -cpp -ip -unroll -scalar_rep "
            opts["CPP_ON_OPTS"] += " -DIFORT -DFFTW"
        if spec.satisfies("%gcc"):
            opts["F90_OPTS"] += " -march=native -ffree-line-length-0"
            if spec.satisfies("%gcc@10:"):
                # The INSTALL file says this will fix the GCC@10 issues
                opts["F90_OPTS"] += " -fallow-argument-mismatch"
                opts["F77_OPTS"] += " -fallow-argument-mismatch"
        filter_file(
            "FCFLAGS = @FCFLAGS@",
            " ".join(["FCFLAGS = @FCFLAGS@", "-cpp", self.compiler.openmp_flag]),
            "src/libXC/src/Makefile.in",
        )
        if spec.satisfies("+mkl"):
            opts["LIB_LPK"] = "-mkl=parallel"
            opts["INC_MKL"] = spec["mkl"].headers.include_flags
            opts["LIB_MKL"] = spec["mkl"].libs.ld_flags
            opts["F90_OPTS"] += spec["mkl"].headers.include_flags
        else:
            opts["LIB_LPK"] = " ".join(
                [
                    spec["lapack"].libs.ld_flags,
                    spec["blas"].libs.ld_flags,
                    self.compiler.openmp_flag,
                ]
            )

        if spec.satisfies("+omp"):
            opts["BUILDSMP"] = "true"

        if spec.satisfies("+mpi"):
            opts["BUILDMPI"] = "true"
            opts["MPIF90"] = spec["mpi"].mpifc
            opts["MPIF90_CPP_OPTS"] = "-DMPI -DMPIRHO -DMPISEC"
            opts["MPIF90_OPTS"] = " ".join(["$(F90_OPTS)", "$(CPP_ON_OPTS) " "$(MPIF90_CPP_OPTS)"])
            opts["MPIF90MT"] = "$(MPIF90)"

            if spec.satisfies("+omp"):
                opts["BUILDMPISMP"] = "true"
                opts["SMPF90_OPTS"] = self.compiler.openmp_flag + " -DUSEOMP"
                opts["SMPF77_OPTS"] = opts["SMPF90_OPTS"]
                opts["SMP_LIBS"] = ""

        else:
            opts["BUILDMPI"] = "false"
        if spec.satisfies("+scalapack"):
            opts["LIB_SCLPK"] = spec["scalapack"].libs.ld_flags
            opts["CPP_SCLPK"] = " -DSCAL "
            opts["MPI_LIBS"] = "$(LIB_SCLPK)"
            opts["MPIF90_CPP_OPTS"] += " $(CPP_SCLPK) "

        opts["USE_SYS_LAPACK"] = "true"
        opts["LIB_FFT"] = "fftlib.a"
        opts["LIB_BZINT"] = "libbzint.a"
        opts["LIBS"] = "$(LIB_ARP) $(LIB_LPK) $(LIB_FFT) $(LIB_BZINT)"

        if "+mpi" not in spec or "+omp" not in spec:
            opts["BUILDMPISMP"] = "false"
        # Write the build/make.inc file
        with open("build/make.inc", "a") as inc:
            for key in opts:
                inc.write("{0} = {1}\n".format(key, opts[key]))

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("species", prefix.species)
        install_tree("tools", prefix.tools)

    def setup_run_environment(self, env):
        env.set("WNHOME", self.prefix)
        env.set("EXCITINGROOT", self.prefix)
        env.set("EXCITINGBIN", self.prefix.bin)
        env.set("EXCITINGTOOLS", self.prefix.tools)
        env.set("EXCITINGSTM", self.prefix.tools.stm)
        env.set("EXCITINGVISUAL", self.prefix.xml.visualizationtemplates)
        env.set("EXCITINGCONVERT", self.prefix.xml.inputfileconverter)
        env.set("TIMEFORMAT", " Elapsed time = %0lR")
        env.set("WRITEMINMAX", "1")
        env.set("USE_SYS_LAPACK", "true")
        env.append_path("PYTHONPATH", self.prefix.tools.stm)
        env.append_path("PATH", self.prefix.tools)
        env.append_path("PATH", self.prefix)
        env.append_path("PATH", self.prefix.tools.stm)
