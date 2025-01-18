# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re

from spack.build_systems import cmake, makefile
from spack.package import *


class Abacus(MakefilePackage, CMakePackage, CudaPackage, ROCmPackage):
    """ABACUS (Atomic-orbital Based Ab-initio Computation at UStc)
    is an open-source computer code package aiming
    for large-scale electronic-structure simulations
    from first principles"""

    maintainers("yizeyi18", "QuantumMisaka", "caic99")

    build_system("cmake", conditional("makefile", when="@:2.3.4"), default="cmake")

    homepage = "http://abacus.ustc.edu.cn/"
    git = "https://github.com/deepmodeling/abacus-develop.git"
    url = "https://github.com/deepmodeling/abacus-develop/archive/refs/tags/v2.2.1.tar.gz"

    license("LGPL-3.0-or-later")

    version("develop", branch="develop")
    version("3.8.0", sha256="6aa57fa4391301af80a5ac641aea1af3f05a614c8ff55f0feb98dc9daf5f2e28")
    version("3.6.1", sha256="ef460417a153216b53e2c45f0bb559cd80ba311ad1b9df3aea6ac7cc30d5f458")
    version("3.5.4", sha256="ab7cbdd07a951da116cc4fe4dfa23e7ac41dda9f35c35d16c267920f267f4722")
    version("3.4.4", sha256="654590f97b2ff3ec49f800da667f24fc34c3ff42b392248b9c88104f8d3bf010")
    version("3.3.4", sha256="f9ef0baa624e39eb4f8a4fd7533d1bdd8f61ee3764a62ac980f51238aa102e38")
    version("3.2.5", sha256="8b96f9e509dedfb3cb43f802715a3ea8bde5d499a525171e314eebe6993c5897")
    version("3.1.4", sha256="4aaf150d74e1c01726f012d23aa1e40e119cac9b8330ae425a29ec3b1040ef1c")
    version("3.0.5", sha256="81ff1b8f10909eeda2d888f97f615e5b92aa26c101a32f36f346f78aa7638ba9")
    version(
        "2.2.3",
        sha256="88dbf6a3bdd907df3e097637ec8e51fde13e2f5e0b44f3667443195481320edf",
        deprecated=True,
    )
    version(
        "2.2.2",
        sha256="4a7cf2ec6e43dd5c53d5f877a941367074f4714d93c1977a719782957916169e",
        deprecated=True,
    )
    version(
        "2.2.1",
        sha256="14feca1d8d1ce025d3f263b85ebfbebc1a1efff704b6490e95b07603c55c1d63",
        deprecated=True,
    )
    version(
        "2.2.0",
        sha256="09d4a2508d903121d29813a85791eeb3a905acbe1c5664b8a88903f8eda64b8f",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant(
        "lcao",
        default=True,
        description="Enable Linear Combinition of Atomic Orbital calculation",
        when="+mpi",
    )
    variant("libxc", default=True, description="Support additional functionals via libxc")
    variant(
        "elpa",
        default=True,
        description="Enable optimised diagonalisation routines from ELPA",
        when="+lcao",
    )
    variant("rocm", default=False, description="(Experimental)Enable rocm support")
    variant(
        "pexsi",
        default=False,
        description="Add PEXSI support for gamma only LCAO calculations",
        when="+lcao",
    )
    # TODO: Add support for
    # LibRI(https://github.com/abacusmodeling/LibRI),
    # LibComm(https://github.com/abacusmodeling/LibComm),
    # Libnpy(https://github.com/llohse/libnpy/),
    # DeePKS(https://github.com/deepmodeling/deepks-kit),
    # DeePMD(https://github.com/deepmodeling/deepmd-kit),
    # LibPAW-interface(https://github.com/wenfei-li/libpaw_interface),
    # At 2024-1-30, none of above have a spack package.

    depends_on("fftw-api@3")
    depends_on("blas")
    depends_on("lapack")

    with when("+mpi"):
        depends_on("mpi", type=("build", "link", "run"))
    with when("+libxc"):
        depends_on("libxc", type=("build", "link"))
    with when("+lcao"):
        depends_on("cereal", type=("build"))
        depends_on("scalapack", type=("link"))
    with when("+elpa"):
        depends_on("elpa", type=("build", "link"))
    with when("+openmp"):
        depends_on("fftw+openmp", when="^[virtuals=fftw-api] fftw")
        depends_on("elpa+openmp", when="+elpa")
        depends_on("openblas threads=openmp", when="^[virtuals=blas] openblas")
        depends_on("openblas threads=openmp", when="^[virtuals=lapack] openblas")
    with when("~openmp"):
        depends_on("elpa~openmp", when="+elpa")
    with when("+pexsi"):
        depends_on("pexsi@2.0.0:", type=("build", "link"))

    requires("%clang", when="+rocm", msg="build with rocm requires rocm compiler")

    conflicts(
        "^blis",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )
    conflicts(
        "^libflame",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )
    conflicts(
        "^amdblis",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )
    conflicts(
        "^amdlibflame",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )
    # netlab-lapack+external-blas do NOT contain libblas.so and not detectable
    # for abacus CMake script.
    conflicts(
        "^[virtuals=lapack] netlib-lapack~external-blas",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )
    conflicts(
        "^netlib-xblas",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )


class MakefileBuilder(makefile.MakefileBuilder):
    build_directory = "source"

    def edit(self, pkg, spec, prefix):
        if spec.satisfies("+openmp"):
            inc_var = "_openmp-"
            system_var = "ELPA_LIB = -L${ELPA_LIB_DIR} -lelpa_openmp -Wl, -rpath=${ELPA_LIB_DIR}"
        else:
            inc_var = "-"
            system_var = "ELPA_LIB = -L${ELPA_LIB_DIR} -lelpa -Wl,-rpath=${ELPA_LIB_DIR}"

        tempInc = """
FORTRAN = ifort
CPLUSPLUS = icpc
CPLUSPLUS_MPI = mpiicpc
LAPACK_DIR = $(MKLROOT)
FFTW_DIR = %s
ELPA_DIR = %s
ELPA_INCLUDE = -I${ELPA_DIR}/include/elpa%s%s
CEREAL_DIR = %s
OBJ_DIR = obj
OBJ_DIR_serial = obj
NP      = 14
""" % (
            spec["fftw"].prefix,
            spec["elpa"].prefix,
            inc_var,
            spec["elpa"].version,
            spec["cereal"].prefix,
        )

        with open(self.build_directory + "/Makefile.vars", "w") as f:
            f.write(tempInc)

        lineList = []
        Pattern1 = re.compile("^ELPA_INCLUDE_DIR")
        Pattern2 = re.compile("^ELPA_LIB\\s*= ")
        with open(self.build_directory + "/Makefile.system", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                elif Pattern1.search(line):
                    pass
                elif Pattern2.search(line):
                    pass
                else:
                    lineList.append(line)
        with open(self.build_directory + "/Makefile.system", "w") as f:
            for i in lineList:
                f.write(i)

        with open(self.build_directory + "/Makefile.system", "a") as f:
            f.write(system_var)

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant("ENABLE_MPI", "mpi"),
            self.define_from_variant("USE_OPENMP", "openmp"),
            self.define_from_variant("USE_ELPA", "elpa"),
            self.define_from_variant("USE_ABACUS_LIBM", "mathlib"),
            self.define_from_variant("ENABLE_LCAO", "lcao"),
            self.define_from_variant("ENABLE_LIBXC", "libxc"),
            self.define_from_variant("USE_ROCM", "rocm"),
            self.define_from_variant("USE_CUDA", "cuda"),
            self.define_from_variant("ENABLE_PEXSI", "pexsi"),
        ]

        blas = spec["blas"]
        lapack = spec["lapack"]
        # fftw = spec["fftw-api"]
        # scalapack = spec["scalapack"] if spec.satisfies("+lcao") else ""
        if blas.name in ["intel-mkl", "intel-parallel-studio", "intel-oneapi-mkl"]:
            args += [self.define("MKLROOT", spec["mkl"].prefix)]
        elif spec.satisfies("@:3.5.4"):
            args.extend(
                [
                    self.define("LAPACK_FOUND", True),
                    self.define(
                        "LAPACK_LIBRARY", lapack.libs
                    ),  # must be single lib with both blas&lapack routines
                ]
            )

        # avoid misdirecting to global visible elpa from apt, dnf, etc.
        if spec.satisfies("+elpa"):
            elpa = spec["elpa"]
            elpa_include = elpa.headers.directories[0]
            args += [self.define("ELPA_INCLUDE_DIRS", elpa_include)]

        if spec.satisfies("+rocm"):
            args += [self.define("COMMIT_INFO", False)]
            args += [self.define("ROCM_PATH", spec["hip"].prefix)]
            # build all c++ part with rocm compiler.
            # cpu and gpu parts can be seperately build, but not done.
            # args += [
            #     self.define(
            #         "CMAKE_CXX_COMPILER",
            #         join_path(spec["llvm-amdgpu"].prefix.bin,"clang++")
            #         )
            #     ]
            # only work for dcu toolkit 23.10 environment, not sure if any other version needs
            args += [
                self.define(
                    "HIP_CXX_COMPILER", join_path(spec["llvm-amdgpu"].prefix.bin, "clang++")
                )
            ]
        return args
