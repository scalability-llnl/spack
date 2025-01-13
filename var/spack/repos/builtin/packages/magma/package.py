# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.util.environment
from spack.package import *


class Magma(CMakePackage, CudaPackage, ROCmPackage):
    """The MAGMA project aims to develop a dense linear algebra library similar
    to LAPACK but for heterogeneous/hybrid architectures, starting with
    current "Multicore+GPU" systems.
    """

    homepage = "https://icl.utk.edu/magma/"
    git = "https://github.com/icl-utk-edu/magma"
    url = "https://icl.utk.edu/projectsfiles/magma/downloads/magma-2.2.0.tar.gz"
    maintainers("stomov", "luszczek", "G-Ragghianti")

    tags = ["e4s"]

    test_requires_compiler = True

    version("master", branch="master")
    version("2.8.0", sha256="f4e5e75350743fe57f49b615247da2cc875e5193cc90c11b43554a7c82cc4348")
    version("2.7.2", sha256="729bc1a70e518a7422fe7a3a54537a4741035a77be3349f66eac5c362576d560")
    version("2.7.1", sha256="d9c8711c047a38cae16efde74bee2eb3333217fd2711e1e9b8606cbbb4ae1a50")
    version("2.7.0", sha256="fda1cbc4607e77cacd8feb1c0f633c5826ba200a018f647f1c5436975b39fd18")
    version("2.6.2", sha256="75b554dab00903e2d10b972c913e50e7f88cbc62f3ae432b5a086c7e4eda0a71")
    version("2.6.1", sha256="6cd83808c6e8bc7a44028e05112b3ab4e579bcc73202ed14733f66661127e213")
    version("2.6.0", sha256="50cdd384f44f06a34469e7125f8b2ffae13c1975d373c3f1510d91be2b7638ec")
    version("2.5.4", sha256="7734fb417ae0c367b418dea15096aef2e278a423e527c615aab47f0683683b67")
    version("2.5.3", sha256="c602d269a9f9a3df28f6a4f593be819abb12ed3fa413bba1ff8183de721c5ef6")
    version("2.5.2", sha256="065feb85558f9dd6f4cc4db36ac633a3f787827fc832d0b578a049a43a195620")
    version("2.5.1", sha256="ce32c199131515336b30c92a907effe0c441ebc5c5bdb255e4b06b2508de109f")
    version("2.5.0", sha256="4fd45c7e46bd9d9124253e7838bbfb9e6003c64c2c67ffcff02e6c36d2bcfa33")
    version("2.4.0", sha256="4eb839b1295405fd29c8a6f5b4ed578476010bf976af46573f80d1169f1f9a4f")
    version("2.3.0", sha256="010a4a057d7aa1e57b9426bffc0958f3d06913c9151463737e289e67dd9ea608")
    version("2.2.0", sha256="df5d4ace417e5bf52694eae0d91490c6bde4cde1b0da98e8d400c5c3a70d83a2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("fortran", default=True, description="Enable Fortran bindings support")
    variant("shared", default=True, description="Enable shared library")
    variant("cuda", default=True, description="Build with CUDA")

    depends_on("blas")
    depends_on("lapack")
    depends_on("cuda@8:", when="@2.5.1: +cuda")  # See PR #14471
    depends_on("hipblas", when="+rocm")
    depends_on("hipsparse", when="+rocm")
    # This ensures that rocm-core matches the hip package version in the case that
    # hip is an external package.
    for ver in [
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
    ]:
        depends_on(f"rocm-core@{ver}", when=f"@2.8.0: +rocm ^hip@{ver}")
    depends_on("python", when="@master", type="build")

    conflicts("~cuda", when="~rocm", msg="magma: Either CUDA or HIP support must be enabled")
    conflicts("+rocm", when="+cuda", msg="magma: CUDA must be disabled to support HIP (ROCm)")
    conflicts("+rocm", when="@:2.5.4", msg="magma: HIP support starts in version 2.6.0")
    conflicts(
        "cuda_arch=none", when="+cuda", msg="magma: Please indicate a CUDA arch value or values"
    )

    # currently not compatible with CUDA-11
    # https://bitbucket.org/icl/magma/issues/22/cuda-11-changes-issue
    # https://bitbucket.org/icl/magma/issues/25/error-cusparsesolveanalysisinfo_t-does-not
    conflicts("^cuda@11:", when="@:2.5.3")

    # currently not compatible with CUDA-12.6
    # https://github.com/icl-utk-edu/magma/issues/7
    conflicts("^cuda@12.6:", when="@:2.8.0")

    # Many cuda_arch values are not yet recognized by MAGMA's CMakeLists.txt
    for target in [10, 11, 12, 13, 21, 32, 52, 53, 61, 62, 72, 86]:
        conflicts(f"cuda_arch={target}")

    # Some cuda_arch values had support added recently
    conflicts("cuda_arch=37", when="@:2.5", msg="magma: cuda_arch=37 needs a version > 2.5")
    conflicts("cuda_arch=60", when="@:2.2", msg="magma: cuda_arch=60 needs a version > 2.2")
    conflicts("cuda_arch=70", when="@:2.2", msg="magma: cuda_arch=70 needs a version > 2.2")
    conflicts("cuda_arch=75", when="@:2.5.0", msg="magma: cuda_arch=75 needs a version > 2.5.0")
    conflicts("cuda_arch=80", when="@:2.5.3", msg="magma: cuda_arch=80 needs a version > 2.5.3")

    patch("ibm-xl.patch", when="@2.2:2.5.0%xl")
    patch("ibm-xl.patch", when="@2.2:2.5.0%xl_r")
    patch("magma-2.3.0-gcc-4.8.patch", when="@2.3.0%gcc@:4.8")
    patch("magma-2.5.0.patch", when="@2.5.0")
    patch("magma-2.5.0-cmake.patch", when="@2.5.0")
    patch("cmake-W.patch", when="@2.5.0:%nvhpc")
    patch("0001-fix-magma-build-error-with-rocm-6.0.0.patch", when="@2.7.2 ^hip@6.0 + rocm")

    @run_before("cmake")
    def generate_gpu_config(self):
        """If not an official release, a generation step is required to build"""
        spec = self.spec

        # 2.6.2rc1 is not an official release
        should_generate = ("@master" in spec) or ("@2.6.2rc1" in spec)

        if not should_generate:
            return

        backend = "cuda" if "+cuda" in spec else "hip"

        gpu_target = ""
        if "+cuda" in spec:
            cuda_archs = spec.variants["cuda_arch"].value
            gpu_target = " ".join(f"sm_{i}" for i in cuda_archs)
        else:
            gpu_target = spec.variants["amdgpu_target"].value

        with open("make.inc", "w") as inc:
            inc.write("FORT = true\n")
            inc.write(f"GPU_TARGET = {gpu_target}\n")
            inc.write(f"BACKEND = {backend}\n")

        make("generate")

    def cmake_args(self):
        spec = self.spec
        define = self.define
        options = [
            define("CMAKE_INSTALL_PREFIX", self.prefix),
            define("CMAKE_INSTALL_NAME_DIR", self.prefix.lib),
            define("BLAS_LIBRARIES", spec["blas"].libs),
            # As of MAGMA v2.3.0, CMakeLists.txt does not use the variable
            # BLAS_LIBRARIES, but only LAPACK_LIBRARIES, so we need to
            # explicitly add blas to LAPACK_LIBRARIES.
            define("LAPACK_LIBRARIES", spec["lapack"].libs + spec["blas"].libs),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        if spec.satisfies("%cce"):
            options.append(define("CUDA_NVCC_FLAGS", "-allow-unsupported-compiler"))

        if "+fortran" in spec:
            options.append(define("USE_FORTRAN", True))
            if spec.satisfies("%xl") or spec.satisfies("%xl_r"):
                options.append(define("CMAKE_Fortran_COMPILER", self.compiler.f77))
            if spec.satisfies("%cce"):
                options.append(define("CMAKE_Fortran_FLAGS", "-ef"))

        if "+cuda" in spec:
            cuda_arch = spec.variants["cuda_arch"].value
            sep = "" if "@:2.2.0" in spec else "_"
            capabilities = " ".join(f"sm{sep}{i}" for i in cuda_arch)
            options.append(define("GPU_TARGET", capabilities))
            archs = ";".join("%s" % i for i in cuda_arch)
            options.append(define("CMAKE_CUDA_ARCHITECTURES", archs))

        if "@2.5.0" in spec:
            options.append(define("MAGMA_SPARSE", False))
            if spec.satisfies("%xl") or spec.satisfies("%xl_r"):
                options.append(define("CMAKE_DISABLE_FIND_PACKAGE_OpenMP", True))

        if "+rocm" in spec:
            options.append(define("MAGMA_ENABLE_HIP", True))
            options.append(define("CMAKE_CXX_COMPILER", spec["hip"].hipcc))
            # See https://github.com/ROCm/rocFFT/issues/322
            if spec.satisfies("^cmake@3.21.0:3.21.2"):
                options.append(define("__skip_rocmclang", True))
            if spec.satisfies("@2.8.0:"):
                options.append(define("ROCM_CORE", spec["rocm-core"].prefix))
        else:
            options.append(define("MAGMA_ENABLE_CUDA", True))

        return options

    @run_after("install")
    def post_install(self):
        install("magmablas/atomics.cuh", self.prefix.include)
        install("control/magma_threadsetting.h", self.prefix.include)
        install("control/pthread_barrier.h", self.prefix.include)
        install("control/magma_internal.h", self.prefix.include)

    test_src_dir = "example"

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [self.test_src_dir])

    def test_c(self):
        """Run C examples"""
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir)
        with working_dir(test_dir):
            pkg_config_path = self.prefix.lib.pkgconfig
            with spack.util.environment.set_env(PKG_CONFIG_PATH=pkg_config_path):

                make("c")
                tests = [
                    ("example_sparse", "sparse solver"),
                    ("example_sparse_operator", "sparse operator"),
                    ("example_v1", "legacy v1 interface"),
                    ("example_v2", "v2 interface"),
                ]

                for test, desc in tests:
                    with test_part(self, f"test_c_{test}", purpose=f"Run {desc} example"):
                        exe = which(test)
                        exe()

                make("clean")

    def test_fortran(self):
        """Run Fortran example"""
        if "+fortran" not in self.spec:
            raise SkipTest("Package must be installed with +fortran")

        test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir)
        with working_dir(test_dir):
            pkg_config_path = self.prefix.lib.pkgconfig
            with spack.util.environment.set_env(PKG_CONFIG_PATH=pkg_config_path):
                make("fortran")
                example_f = which("example_f")
                example_f()
                make("clean")
