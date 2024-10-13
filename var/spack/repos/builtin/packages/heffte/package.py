# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Heffte(CMakePackage, CudaPackage, ROCmPackage):
    """Highly Efficient FFT for Exascale"""

    homepage = "https://github.com/icl-utk-edu/heffte/"
    url = "https://github.com/icl-utk-edu/heffte/archive/refs/tags/v2.4.0.tar.gz"
    git = "https://github.com/icl-utk-edu/heffte/"

    maintainers("mkstoyanov", "G-Ragghianti")
    tags = ["e4s", "ecp"]

    test_requires_compiler = True

    license("BSD-3-Clause")

    version("develop", branch="master")
    version("2.4.0", sha256="02310fb4f9688df02f7181667e61c3adb7e38baf79611d80919d47452ff7881d")
    version("2.3.0", sha256="63db8c9a8822211d23e29f7adf5aa88bb462c91d7a18c296c3ef3a06be8d6171")
    version("2.2.0", sha256="332346d5c1d1032288d09839134c79e4a9704e213a2d53051e96c3c414c74df0")
    version("2.1.0", sha256="63b8ea45a220afc4fa0b14769c0dd291e614a2fe9d5a91c50d28f16ee29b3f1c")
    version(
        "2.0.0",
        sha256="b575fafe19a635265904ca302d48e778341b1567c055ea7f2939c8c6718f7212",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch("cmake-magma-v230.patch", when="@2.3.0")
    patch("fortran200.patch", when="@2.0.0")

    depends_on("cmake@3.10:", when="@:2.3.0", type=("build", "run"))
    depends_on("cmake@3.19:", when="@2.4.0:", type=("build", "run"))
    depends_on("cmake@3.21:", when="@2.4.0:+rocm", type=("build", "run"))

    variant("shared", default=True, description="Builds with shared libraries")
    variant("fftw", default=False, description="Builds with support for FFTW backend")
    variant(
        "sycl",
        default=False,
        when="%oneapi",
        description="Builds with support for oneAPI SYCL+oneMKL backend",
    )
    variant("mkl", default=False, description="Builds with support for MKL backend")
    variant("magma", default=False, description="Use helper methods from the UTK MAGMA library")
    variant("python", default=False, description="Install the Python bindings")
    variant("fortran", default=False, description="Install the Fortran modules")

    depends_on("python@3.0:", when="+python", type=("build", "run"))
    depends_on("py-mpi4py", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-numba", when="+python+cuda", type=("build", "run"))
    extends("python", when="+python", type=("build", "run"))

    conflicts("^openmpi~cuda", when="+cuda")  # +cuda requires CUDA enabled OpenMPI
    conflicts("~cuda~rocm", when="+magma")  # magma requires CUDA or HIP
    conflicts("+rocm", when="@:2.1.0")  # heffte+rocm is in in development in spack

    depends_on("mpi", type=("build", "run"))

    depends_on("fftw@3.3.8:", when="+fftw", type=("build", "run"))
    depends_on("intel-oneapi-mkl", when="+mkl", type=("build", "run"))
    depends_on("cuda@8.0:", when="+cuda", type=("build", "run"))
    depends_on("hip@3.8.0:", when="+rocm", type=("build", "run"))
    depends_on("rocfft@3.8.0:", when="+rocm", type=("build", "run"))
    depends_on("hip@5.2.3:", when="@2.4.0:+rocm", type=("build", "run"))
    depends_on("rocfft@5.2.3:", when="@2.4.0:+rocm", type=("build", "run"))
    depends_on("magma@2.5.3:", when="+cuda+magma", type=("build", "run"))
    depends_on("magma+rocm@2.6.1:", when="+magma+rocm @2.1:", type=("build", "run"))
    depends_on("rocblas@3.8:", when="+magma+rocm", type=("build", "run"))
    depends_on("rocsparse@3.8:", when="+magma+rocm", type=("build", "run"))
    depends_on("hipblas@3.8:", when="+magma+rocm", type=("build", "run"))
    depends_on("hipsparse@3.8:", when="+magma+rocm", type=("build", "run"))
    depends_on("intel-oneapi-mkl@2023.2.0:", when="+sycl", type=("build", "run"))
    depends_on("intel-oneapi-mpi@2021.10.0:", when="+sycl", type=("build", "run"))

    examples_src_dir = "examples"

    def cmake_args(self):
        args = [
            "-DHeffte_SEQUENTIAL_TESTING=ON",
            "-DHeffte_ENABLE_TESTING=ON",
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("Heffte_ENABLE_CUDA", "cuda"),
            self.define_from_variant("Heffte_ENABLE_ROCM", "rocm"),
            self.define_from_variant("Heffte_ENABLE_ONEAPI", "sycl"),
            self.define_from_variant("Heffte_ENABLE_FFTW", "fftw"),
            self.define_from_variant("Heffte_ENABLE_MKL", "mkl"),
            self.define_from_variant("Heffte_ENABLE_MAGMA", "magma"),
            self.define_from_variant("Heffte_ENABLE_FORTRAN", "fortran"),
            self.define_from_variant("Heffte_ENABLE_PYTHON", "python"),
        ]

        if self.spec.satisfies("+cuda") and self.spec.satisfies("@:2.3.0"):
            cuda_arch = self.spec.variants["cuda_arch"].value
            if len(cuda_arch) > 0 or cuda_arch[0] != "none":
                nvcc_flags = ""
                for nvflag in self.cuda_flags(cuda_arch):
                    nvcc_flags += "{0};".format(nvflag)

                args.append("-DCUDA_NVCC_FLAGS={0}".format(nvcc_flags))
                archs = ";".join(cuda_arch)
                args.append("-DCMAKE_CUDA_ARCHITECTURES=%s" % archs)

        if self.spec.satisfies("+rocm"):
            args.append("-DCMAKE_CXX_COMPILER={0}".format(self.spec["hip"].hipcc))

            rocm_arch = self.spec.variants["amdgpu_target"].value
            if "none" not in rocm_arch:
                args.append("-DCMAKE_CXX_FLAGS={0}".format(self.hip_flags(rocm_arch)))

            # See https://github.com/ROCm/rocFFT/issues/322
            if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
                args.append(self.define("__skip_rocmclang", "ON"))

        return args

    @run_after("install")
    def setup_smoke_test(self):
        if self.spec.satisfies("@:2.2.0"):
            return
        install_tree(
            self.prefix.share.heffte.testing, join_path(install_test_root(self), "testing")
        )

    def test_make_test(self):
        """build and run make(test)"""

        if self.spec.satisfies("@:2.2.0"):
            raise SkipTest("Test is not supported for versions @:2.2.0")

        # using the tests copied from <prefix>/share/heffte/testing
        cmake_dir = self.test_suite.current_test_cache_dir.testing

        options = [cmake_dir]
        options.append(self.define("Heffte_DIR", self.spec.prefix.lib.cmake.Heffte))
        if self.spec.satisfies("+rocm"):
            # path name is 'hsa-runtime64' but python cannot have '-' in variable name
            hsa_runtime = join_path(self.spec["hsa-rocr-dev"].prefix.lib.cmake, "hsa-runtime64")
            options.extend(
                [
                    self.define("hip_DIR", self.spec["hip"].prefix.lib.cmake.hip),
                    self.define(
                        "AMDDeviceLibs_DIR",
                        self.spec["llvm-amdgpu"].prefix.lib.cmake.AMDDeviceLibs,
                    ),
                    self.define("amd_comgr_DIR", self.spec["comgr"].prefix.lib.cmake.amd_comgr),
                    self.define("hsa-runtime64_DIR", hsa_runtime),
                    self.define("HSA_HEADER", self.spec["hsa-rocr-dev"].prefix.include),
                    self.define("rocfft_DIR", self.spec["rocfft"].prefix.lib.cmake.rocfft),
                ]
            )

        # Provide the root directory of the MPI installation.
        options.append(self.define("MPI_HOME", self.spec["mpi"].prefix))

        cmake = which(self.spec["cmake"].prefix.bin.cmake)
        cmake(*options)

        make = which("make")
        make()
        make("test")
