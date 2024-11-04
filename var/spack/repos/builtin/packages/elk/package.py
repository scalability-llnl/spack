# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Elk(MakefilePackage):
    """An all-electron full-potential linearised augmented-plane wave
    (FP-LAPW) code with many advanced features."""

    homepage = "https://elk.sourceforge.io/"
    url = "https://sourceforge.net/projects/elk/files/elk-3.3.17.tgz"

    license("LGPL-3.0-or-later")

    version("8.3.22", sha256="1c31f09b7c09d6b24e775d4f0d5e1e8871f95a7656ee4ca21ac17dbe7ea16277")
    version("7.2.42", sha256="73f03776dbf9b2147bfcc5b7c062af5befa0944608f6fc4b6a1e590615400fc6")
    version("7.1.14", sha256="7c2ff30f4b1d72d5dc116de9d70761f2c206700c69d85dd82a17a5a6374453d2")
    version("7.0.12", sha256="9995387c681d0e5a9bd52cb274530b23c0370468b6be86f6c90a6ec445cb8a01")
    version(
        "3.3.17",
        sha256="c9b87ae4ef367ed43afc2d43eb961745668e40670995e8e24c13db41b7e85d73",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # what linear algebra packages to use? the choices are
    # internal - use internal libraries
    # generic  - use spack-provided blas and lapack
    # openblas - use openblas specifically, with special support for multithreading.
    # mkl - use mkl specifically, with special support for multithreading
    # should be used with fft=mkl
    # blis - use internal lapack and blas implementation from blis
    variant(
        "linalg",
        default="internal",
        multi=False,
        description="Build with custom BLAS library",
        values=("internal", "generic", "openblas", "mkl", "blis"),
    )
    # what FFT package to use? The choices are
    # internal - use internal library
    # fftw - fftw3 with special code
    # mkl  - use mklr with fft code
    # should be used with linalg=mkls
    variant(
        "fft",
        default="internal",
        multi=False,
        description="Build with custom FFT library",
        values=("internal", "fftw", "mkl"),
    )
    #  check that if fft=mkl then linalg=mkl and vice versa.

    conflicts("linalg=mkl", when="fft=fftw")
    conflicts("linalg=mkl", when="fft=internal")
    conflicts("linalg=blis", when="@:3")
    conflicts("fft=mkl", when="linalg=internal")
    conflicts("fft=mkl", when="linalg=generic")
    conflicts("fft=mkl", when="linalg=openblas")
    conflicts("fft=mkl", when="linalg=blis")

    variant("mpi", default=True, description="Enable MPI parallelism")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("libxc", default=True, description="Link to Libxc functional library")
    variant("w90", default=False, description="wannier90 support, requires wannier90 library")

    depends_on("blas", when="linalg=generic")
    depends_on("lapack", when="linalg=generic")

    depends_on("mkl", when="linalg=mkl")
    with when("linalg=mkl +openmp"):
        depends_on("intel-mkl threads=openmp", when="^[virtuals=mkl] intel-mkl")
        depends_on("intel-oneapi-mkl threads=openmp", when="^[virtuals=mkl] intel-oneapi-mkl")
        depends_on(
            "intel-parallel-studio threads=openmp", when="^[virtuals=mkl] intel-parallel-studio"
        )

    depends_on("openblas", when="linalg=openblas")
    depends_on("openblas threads=openmp", when="linalg=openblas +openmp")

    depends_on("blis", when="linalg=blis")
    depends_on("blis threads=openmp", when="linalg=blis +openmp")

    depends_on("fftw", when="fft=fftw")
    depends_on("fftw +openmp", when="fft=fftw +openmp")
    depends_on("mkl", when="fft=mkl")

    depends_on("mpi@2:", when="+mpi")
    depends_on("libxc@5:", when="@7:+libxc")
    depends_on("libxc@:3", when="@:3+libxc")
    depends_on("wannier90", when="+w90")

    # Cannot be built in parallel
    parallel = False

    def edit(self, spec, prefix):
        # Dictionary of configuration options with default values assigned
        config = {
            "MAKE": "make",
            "AR": "ar",
            "LIB_LPK": "lapack.a blas.a",
            "LIB_FFT": "fftlib.a",
            "SRC_MPI": "mpi_stub.f90",
            "SRC_MKL": "mkl_stub.f90",
            "SRC_OBLAS": "oblas_stub.f90",
            "SRC_OMP": "omp_stub.f90",
            "SRC_BLIS": "blis_stub.f90",
            "SRC_libxc": "libxcifc_stub.f90",
            "SRC_FFT": "zfftifc.f90",
            "SRC_W90S": "w90_stub.f90",
            "F90": spack_fc,
            "F77": spack_f77,
        }
        # Compiler-specific flags

        flags = ""
        if self.compiler.name == "intel":
            flags = "-O3 -ip -unroll -no-prec-div"
        elif self.compiler.name == "gcc":
            flags = "-O3 -ffast-math -funroll-loops"
            if spec.satisfies("%gcc@10:"):
                flags += " -fallow-argument-mismatch "
        elif self.compiler.name == "pgi":
            flags = "-O3 -lpthread"
        elif self.compiler.name == "g95":
            flags = "-O3 -fno-second-underscore"
        elif self.compiler.name == "nag":
            flags = "-O4 -kind=byte -dusty -dcfuns"
        elif self.compiler.name == "xl":
            flags = "-O3"
        config["F90_OPTS"] = flags
        config["F77_OPTS"] = flags

        if spec.satisfies("+mpi"):
            config["F90"] = spec["mpi"].mpifc
            config["F77"] = spec["mpi"].mpif77
            config["SRC_MPI"] = " "
        else:
            config["F90"] = spack_fc
            config["F77"] = spack_f77
            config["SRC_MPI"] = "mpi_stub.f90"

        # OpenMP support
        if spec.satisfies("+openmp"):
            config["F90_OPTS"] += " " + self.compiler.openmp_flag
            config["F77_OPTS"] += " " + self.compiler.openmp_flag
            config["SRC_OMP"] = " "

        # BLAS/LAPACK support
        # Note: openblas must be compiled with OpenMP support
        # if the +openmp variant is chosen
        if spec.satisfies("linalg=internal"):
            self.build_targets.append("blas")
            self.build_targets.append("lapack")
        if spec.satisfies("linalg=generic"):
            blas = spec["blas"].libs.joined()
            lapack = spec["lapack"].libs.joined()
            config["LIB_LPK"] = " ".join([lapack, blas])
        if spec.satisfies("linalg=openblas"):
            config["LIB_LPK"] = spec["openblas"].libs.ld_flags
            config["SRC_OBLAS"] = " "
        if spec.satisfies("linalg=mkl"):
            config["LIB_LPK"] = spec["mkl"].libs.ld_flags
            config["SRC_MKL"] = " "
        if spec.satisfies("linalg=blis"):
            config["LIB_LPK"] = " ".join(["lapack.a ", spec["blis"].libs.ld_flags])
            config["SRC_BLIS"] = " "
        # FFT
        if spec.satisfies("fft=internal"):
            self.build_targets.append("fft")
        elif spec.satisfies("fft=fftw"):
            config["LIB_FFT"] = spec["fftw"].libs.ld_flags
            config["SRC_FFT"] = "zfftifc_fftw.f90"
        elif spec.satisfies("fft=mkl"):
            config["LIB_FFT"] = spec["mkl"].libs.ld_flags
            config["SRC_FFT"] = "mkl_dfti.f90 zfftifc_mkl.f90"
            cp = which("cp")
            mkl_prefix = spec["mkl"].prefix
            if spec.satisfies("^intel-mkl"):
                mkl_prefix = mkl_prefix.mkl
            cp(
                join_path(mkl_prefix.include, "mkl_dfti.f90"),
                join_path(self.build_directory, "src"),
            )

        # Define targets
        self.build_targets.append("elk")
        print(self.build_targets)
        # Libxc support
        if spec.satisfies("+libxc"):
            config["LIB_libxc"] = " ".join(
                [
                    join_path(spec["libxc"].prefix.lib, "libxcf90.so"),
                    join_path(spec["libxc"].prefix.lib, "libxc.so"),
                ]
            )
            if self.spec.satisfies("@7:"):
                config["SRC_libxc"] = "libxcf90.f90 libxcifc.f90"
            else:
                config["SRC_libxc"] = "libxc_funcs.f90 libxc.f90 libxcifc.f90"

        # Write configuration options to include file
        with open("make.inc", "w") as inc:
            for key in config:
                inc.write("{0} = {1}\n".format(key, config[key]))

    def build(self, spec, prefix):
        with working_dir(self.build_directory + "/src"):
            make(*self.build_targets)
            make("-C", "eos")
            make("-C", "spacegroup")

    def install(self, spec, prefix):
        # The Elk Makefile does not provide an install target
        mkdir(prefix.bin)

        install("src/elk", prefix.bin)
        install("src/eos/eos", prefix.bin)
        install("src/spacegroup/spacegroup", prefix.bin)

        install_tree("examples", join_path(prefix, "examples"))
        install_tree("species", join_path(prefix, "species"))
