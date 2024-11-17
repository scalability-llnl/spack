# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class AoclSparse(CMakePackage):
    """AOCL-Sparse is a library that contains basic linear algebra subroutines
    for sparse matrices and vectors optimized for AMD EPYC family of processors.
    It is designed to be used with C and C++. Current functionality of sparse
    library supports SPMV function with CSR and ELLPACK formats.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-Sparse license agreement.
    You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/sparse/eula/sparse-libraries-4-2-eula.html
    https://www.amd.com/en/developer/aocl/sparse/eula/sparse-libraries-eula.html
    """

    _name = "aocl-sparse"
    homepage = "https://www.amd.com/en/developer/aocl/sparse.html"
    git = "https://github.com/amd/aocl-sparse"
    url = "https://github.com/amd/aocl-sparse/archive/3.0.tar.gz"

    maintainers("amd-toolchain-support")

    license("MIT")

    version(
        "5.0",
        sha256="7528970f41ae60563df9fe1f8cc74a435be1566c01868a603ab894e9956c3c94",
        preferred=True,
    )
    version("4.2", sha256="03cd67adcfea4a574fece98b60b4aba0a6e5a9c8f608ff1ccc1fb324a7185538")
    version("4.1", sha256="35ef437210bc25fdd802b462eaca830bfd928f962569b91b592f2866033ef2bb")
    version("4.0", sha256="68524e441fdc7bb923333b98151005bed39154d9f4b5e8310b5c37de1d69c2c3")
    version("3.2", sha256="db7d681a8697d6ef49acf3e97e8bec35b048ce0ad74549c3b738bbdff496618f")
    version("3.1", sha256="8536f06095c95074d4297a3d2910654085dd91bce82e116c10368a9f87e9c7b9")
    version("3.0", sha256="1d04ba16e04c065051af916b1ed9afce50296edfa9b1513211a7378e1d6b952e")
    version("2.2", sha256="33c2ed6622cda61d2613ee63ff12c116a6cd209c62e54307b8fde986cd65f664")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared library")
    variant("ilp64", default=False, description="Build with ILP64 support")
    variant("examples", default=False, description="Build sparse examples")
    variant("unit_tests", default=False, description="Build sparse unit tests")
    variant("benchmarks", default=False, description="Build Build benchmarks")
    variant(
        "avx",
        default=False,
        when="@4.0: target=zen4:",
        description="Enable experimental AVX512 support",
    )
    variant("openmp", default=True, when="@4.2:", description="Enable OpenMP support")

    for vers in ["4.1", "4.2", "5.0"]:
        with when(f"@={vers}"):
            depends_on(f"amdblis@={vers}")
            depends_on(f"amdlibflame@={vers}")
            if Version(vers) >= Version("4.2"):
                depends_on(f"aocl-utils@={vers}")

    depends_on("amdblis threads=openmp", when="+openmp")
    depends_on("amdlibflame threads=openmp", when="+openmp")
    depends_on("amdblis threads=none", when="~openmp")
    depends_on("amdlibflame threads=none", when="~openmp")
    depends_on("boost", when="+benchmarks")
    depends_on("boost", when="@2.2")
    depends_on("cmake@3.22:", type="build")

    @property
    def libs(self):
        """find libaoclsparse libs function"""
        return find_libraries(
            "libaoclsparse", root=self.prefix, shared="+shared" in self.spec, recursive=True
        )

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """

        build_directory = self.stage.source_path

        if self.spec.variants["build_type"].value == "Debug":
            build_directory = join_path(build_directory, "build", "debug")
        else:
            build_directory = join_path(build_directory, "build", "release")

        return build_directory

    def cmake_args(self):
        """Runs ``cmake`` in the build directory"""
        spec = self.spec

        args = []
        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("BUILD_CLIENTS_SAMPLES", "examples"))
        args.append(self.define_from_variant("BUILD_CLIENTS_TESTS", "unit_tests"))
        args.append(self.define_from_variant("BUILD_CLIENTS_BENCHMARKS", "benchmarks"))
        args.append(self.define_from_variant("USE_AVX512", "avx"))

        if spec.satisfies("@3.0:"):
            args.append(self.define_from_variant("BUILD_ILP64", "ilp64"))

        if spec.satisfies("@4.0:"):
            args.append(f"-DAOCL_BLIS_LIB={self.spec['amdblis'].libs}")
            args.append("-DAOCL_BLIS_INCLUDE_DIR={0}/blis".format(spec["amdblis"].prefix.include))
            args.append(f"-DAOCL_LIBFLAME={spec['amdlibflame'].libs}")
            args.append(
                "-DAOCL_LIBFLAME_INCLUDE_DIR={0}".format(spec["amdlibflame"].prefix.include)
            )

        if spec.satisfies("@4.2:"):
            args.append(f"-DAOCL_UTILS_LIB={spec['aocl-utils'].libs}")
            args.append("-DAOCL_UTILS_INCLUDE_DIR={0}".format(spec["aocl-utils"].prefix.include))

        args.append(self.define_from_variant("SUPPORT_OMP", "openmp"))

        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check(self):
        """Simple test to test the built library by running
        one of the aocl-sparse examples, after compiling the
        library with benchmarks.
        """
        dso_suffix = "so" if "+shared" in self.spec else "a"

        if self.spec.variants["build_type"].value == "Debug":
            lib_path = join_path(
                self.build_directory, "library", "libaoclsparse-d.{0}".format(dso_suffix)
            )
        else:
            lib_path = join_path(
                self.build_directory, "library", "libaoclsparse.{0}".format(dso_suffix)
            )

        test_bench_bin = join_path(self.build_directory, "tests", "staging", "aoclsparse-bench")
        test_args = " --function=csrmv --precision=d "
        test_args += "--sizem=1000 --sizen=1000 --sizennz=4000 --verify=1 "
        os.system(test_bench_bin + test_args + lib_path)
