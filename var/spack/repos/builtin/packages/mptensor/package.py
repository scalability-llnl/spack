# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mptensor(CMakePackage):
    """mptensor is parallel C++ libarary for tensor calculations.
    It provides similar interfaces as Numpy and Scipy in Python."""

    homepage = "https://github.com/smorita/mptensor"
    url = "https://github.com/smorita/mptensor/archive/v0.3.0.tar.gz"

    license("LGPL-3.0-or-later")

    version("0.3.0", sha256="819395a91551bddb77958615042fcb935a4b67ee37f912b9a2ca5b49c71befae")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=False, description="Build with MPI library")
    variant("doc", default=False, description="build documentation with Doxygen")

    depends_on("cmake@3.6:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack", when="+mpi")
    depends_on("doxygen@:1.8.11", type="build", when="+doc")

    test_requires_compiler = True

    def cmake_args(self):
        spec = self.spec
        options = []

        if "+mpi" in spec:
            options.extend(
                [
                    "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
                    "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
                    "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
                    "-DSCALAPACK_LIBRARIES=%s" % spec["scalapack"].libs,
                ]
            )
        else:
            options.extend(
                [
                    "-DCMAKE_C_COMPILER=%s" % spack_cc,
                    "-DCMAKE_CXX_COMPILER=%s" % spack_cxx,
                    "-DCMAKE_Fortran_COMPILER=%s" % spack_fc,
                ]
            )

        blas = spec["blas"].libs
        lapack = spec["lapack"].libs
        options.extend(
            [
                "-DLAPACK_LIBRARIES=%s" % ";".join(lapack),
                "-DBLAS_LIBRARIES=%s" % ";".join(blas),
                self.define_from_variant("ENABLE_MPI", "mpi"),
                self.define_from_variant("BUILD_DOC", "doc"),
            ]
        )

        return options

    @run_after("install")
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""

        # Tests only supported when spec built with mpi
        if "+mpi" not in self.spec:
            print("Skipping copy of stand-alone test files: requires +mpi build")
            return

        cache_extra_test_sources(self, ".")

        # Clean cached makefiles now so only done once
        print("Converting cached Makefile for stand-alone test use")
        with working_dir(join_path(install_test_root(self), "tests")):
            make("clean")
            makefile = FileFilter("Makefile")
            makefile.filter("g++", f"{spack_cxx}", string=True)

        print("Converting cached Makefile.option for stand-alone test use")
        with working_dir(join_path(install_test_root(self))):
            makefile = FileFilter("Makefile.option")
            makefile.filter("CXX =.*", f"CXX ={self.spec['mpi'].mpicxx}")
            makefile.filter("CXXFLAGS =.*", f"CXXFLAGS ={self.compiler.cxx11_flag}")

    def test_tensor_test(self):
        """build and run tensor_test"""
        if "+mpi" not in self.spec:
            raise SkipTest("Package must be installed with +mpi")

        math_libs = self.spec["scalapack"].libs + self.spec["lapack"].libs + self.spec["blas"].libs

        with working_dir(self.test_suite.current_test_cache_dir.tests):
            make = which("make")
            make(f"LDFLAGS={math_libs.ld_flags}")

            mpirun = which(self.spec["mpi"].prefix.bin.mpirun)
            mpirun("-n", "1", "tensor_test.out")

            # Test of mptensor has checker
            # and checker is abort when check detect any errors.
            print("Test of mptensor PASSED !")
