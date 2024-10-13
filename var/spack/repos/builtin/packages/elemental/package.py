# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.spec import UnsupportedCompilerError


class Elemental(CMakePackage):
    """Elemental: Distributed-memory dense and sparse-direct linear algebra
    and optimization library."""

    homepage = "https://libelemental.org"
    url = "https://github.com/elemental/Elemental/archive/v0.87.7.tar.gz"
    git = "https://github.com/elemental/Elemental.git"

    license("Apache-2.0")

    version("develop", branch="master")
    version("0.87.7", sha256="7becfdbc223e9c72e65ae876d842c48d2037d13f83e9f41cea285e21b840d7d9")
    version("0.87.6", sha256="b597987c99ddd3462e0619524c5b7f711177ae8ae541b1b961e11d96e15afc64")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("hybrid", default=True, description="Make use of OpenMP within MPI packing/unpacking")
    variant(
        "openmp_blas", default=False, description="Use OpenMP for threading in the BLAS library"
    )
    variant("c", default=False, description="Build C interface")
    variant("parmetis", default=False, description="Enable ParMETIS")
    variant("quad", default=False, description="Enable quad precision")
    variant("int64", default=False, description="Use 64bit integers")
    variant("cublas", default=False, description="Enable cuBLAS for local BLAS operations")
    # When this variant is set remove the normal dependencies since
    # Elemental has to build BLAS and ScaLAPACK internally
    variant(
        "int64_blas",
        default=False,
        description="Use 64bit integers for BLAS." " Requires local build of BLAS library.",
    )
    variant("scalapack", default=False, description="Build with ScaLAPACK library")
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
    variant(
        "blas",
        default="openblas",
        values=("openblas", "mkl", "accelerate", "essl"),
        description="Enable the use of OpenBlas/MKL/Accelerate/ESSL",
    )
    variant(
        "mpfr",
        default=False,
        description="Support GNU MPFR's" "arbitrary-precision floating-point arithmetic",
    )

    # Note that #1712 forces us to enumerate the different blas variants
    depends_on("blas", when="~openmp_blas ~int64_blas")
    # Hack to forward variant to openblas package
    depends_on("openblas", when="blas=openblas ~openmp_blas ~int64_blas")
    # Allow Elemental to build internally when using 8-byte ints
    depends_on("openblas threads=openmp", when="blas=openblas +openmp_blas ~int64_blas")

    depends_on("intel-mkl", when="blas=mkl")
    depends_on("intel-mkl threads=openmp", when="blas=mkl +openmp_blas")
    depends_on("intel-mkl@2017.1 +ilp64", when="blas=mkl +int64_blas")

    depends_on("veclibfort", when="blas=accelerate")

    depends_on("essl", when="blas=essl")
    depends_on("essl threads=openmp", when="blas=essl +openmp_blas")

    # Note that this forces us to use OpenBLAS until #1712 is fixed
    depends_on("lapack", when="blas=openblas ~openmp_blas")
    depends_on("netlib-lapack +external-blas", when="blas=essl")

    depends_on("metis")
    depends_on("metis +int64", when="+int64")
    depends_on("mpi")
    # Allow Elemental to build internally when using 8-byte ints
    depends_on("scalapack", when="+scalapack ~int64_blas")
    depends_on("gmp", when="+mpfr")
    depends_on("mpc", when="+mpfr")
    depends_on("mpfr", when="+mpfr")

    patch("elemental_cublas.patch", when="+cublas")
    patch("cmake_0.87.7.patch", when="@0.87.7")

    @property
    def libs(self):
        shared = True if "+shared" in self.spec else False
        return find_libraries("libEl", root=self.prefix, shared=shared, recursive=True)

    def cmake_args(self):
        spec = self.spec

        if spec.satisfies("@:0.87.7") and spec.satisfies("%intel@:17.0.2"):
            raise UnsupportedCompilerError(
                "Elemental {0} has a known bug with compiler: {1} {2}".format(
                    spec.version, spec.compiler.name, spec.compiler.version
                )
            )

        args = [
            "-DCMAKE_INSTALL_MESSAGE:STRING=LAZY",
            "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
            "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
            "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
            "-DEL_PREFER_OPENBLAS:BOOL=TRUE",
            "-DEL_DISABLE_SCALAPACK:BOOL=%s" % ("~scalapack" in spec),
            "-DBUILD_SHARED_LIBS:BOOL=%s" % ("+shared" in spec),
            "-DEL_HYBRID:BOOL=%s" % ("+hybrid" in spec),
            "-DEL_C_INTERFACE:BOOL=%s" % ("+c" in spec),
            "-DEL_DISABLE_PARMETIS:BOOL=%s" % ("~parmetis" in spec),
            "-DEL_DISABLE_QUAD:BOOL=%s" % ("~quad" in spec),
            "-DEL_USE_64BIT_INTS:BOOL=%s" % ("+int64" in spec),
            "-DEL_USE_64BIT_BLAS_INTS:BOOL=%s" % ("+int64_blas" in spec),
            "-DEL_DISABLE_MPFR:BOOL=%s" % ("~mpfr" in spec),
        ]

        if self.spec.satisfies("%intel"):
            ifort = env["SPACK_F77"]
            intel_bin = os.path.dirname(ifort)
            intel_root = os.path.dirname(intel_bin)
            libfortran = find_libraries("libifcoremt", root=intel_root, recursive=True)
        elif self.spec.satisfies("%gcc"):
            # see <stage_folder>/debian/rules as an example:
            mpif77 = Executable(spec["mpi"].mpif77)
            libfortran = LibraryList(
                mpif77("--print-file-name", "libgfortran.%s" % dso_suffix, output=str).strip()
            )
        elif self.spec.satisfies("%xl") or self.spec.satisfies("%xl_r"):
            xl_fort = env["SPACK_F77"]
            xl_bin = os.path.dirname(xl_fort)
            xl_root = os.path.dirname(xl_bin)
            libfortran = find_libraries("libxlf90_r", root=xl_root, recursive=True)
        else:
            libfortran = None

        if libfortran:
            args.append("-DGFORTRAN_LIB=%s" % libfortran.libraries[0])

        # If using 64bit int BLAS libraries, elemental has to build
        # them internally
        if spec.satisfies("+int64_blas"):
            args.extend(
                [
                    "-DEL_BLAS_SUFFIX:STRING={0}".format(
                        ("_64_" if "+int64_blas" in spec else "_")
                    ),
                    "-DCUSTOM_BLAS_SUFFIX:BOOL=TRUE",
                ]
            ),
            if spec.satisfies("+scalapack"):
                args.extend(
                    [
                        "-DEL_LAPACK_SUFFIX:STRING={0}".format(
                            ("_64_" if "+int64_blas" in spec else "_")
                        ),
                        "-DCUSTOM_LAPACK_SUFFIX:BOOL=TRUE",
                    ]
                ),
        else:
            math_libs = spec["lapack"].libs + spec["blas"].libs

            if spec.satisfies("+scalapack"):
                math_libs = spec["scalapack"].libs + math_libs

            args.extend(["-DMATH_LIBS:STRING={0}".format(math_libs.ld_flags)])

        return args
