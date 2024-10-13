# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tasmanian(CMakePackage, CudaPackage, ROCmPackage):
    """The Toolkit for Adaptive Stochastic Modeling and Non-Intrusive
    ApproximatioN is a robust library for high dimensional integration and
    interpolation as well as parameter calibration."""

    homepage = "https://ornl.github.io/TASMANIAN/stable/"
    url = "https://github.com/ORNL/TASMANIAN/archive/v8.0.tar.gz"
    git = "https://github.com/ORNL/TASMANIAN.git"

    tags = ["e4s"]
    maintainers("mkstoyanov")

    test_requires_compiler = True

    version("develop", branch="master")

    version("8.0", sha256="248c941346150bf6cfb386ba86b69bd4697f4fc93bff0e8d5f57e555614fd534")
    version("7.9", sha256="decba62e6bbccf1bc26c6e773a8d4fd51d7f3e3e534ddd386ec41300694ce5cc")
    version("7.7", sha256="85fb3a7b302ea21a3b700712767a59a623d9ab93da03308fa47d4413654c3878")
    version("7.5", sha256="d621bd36dced4db86ef638693ba89b336762e7a3d7fedb3b5bcefb03390712b3")

    # Tasmanian is backwards compatible, no need to use 7.3 from back in 2020
    version(
        "7.3",
        sha256="5bd1dd89cc5c84506f6900b6569b17e50becd73eb31ec85cfa11d6f1f912c4fa",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("xsdkflags", default=False, description="enable XSDK defaults for Tasmanian")

    variant("openmp", default=False, description="add OpenMP support to Tasmanian")

    variant("blas", default=False, description="add BLAS support to Tasmanian")

    variant("mpi", default=False, description="add MPI support to Tasmanian")

    variant("cuda", default=False, description="add CUDA support to Tasmanian")

    variant("rocm", default=False, description="add ROCm support to Tasmanian")

    variant("magma", default=False, description="add UTK MAGMA support to Tasmanian")

    variant("python", default=False, description="add Python binding for Tasmanian")

    variant("fortran", default=False, description="add Fortran 2003 interface to Tasmanian")

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release"),
    )

    depends_on("cmake@3.10:", type=("build", "run"), when="@7.0:")
    depends_on("cmake@3.22:", type=("build", "run"), when="@8.0:")

    depends_on("python@3.0:", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))

    extends("python", when="+python", type=("build", "run"))

    depends_on("mpi", when="+mpi", type=("build", "run"))  # openmpi 2 and 3 tested

    depends_on("blas", when="+blas", type=("build", "run"))  # openblas 0.2.18 or newer
    depends_on("lapack", when="+blas @7.1:", type=("build", "run"))  # lapack used since 7.1

    depends_on("cuda@10.0:", when="+cuda", type=("build", "run"))
    depends_on("cuda@10.0:", when="+magma", type=("build", "run"))

    depends_on("hip@5.0:", when="+rocm", type=("build", "run"))
    depends_on("rocblas@5.0:", when="+rocm", type=("build", "run"))
    depends_on("rocsparse@5.0:", when="+rocm", type=("build", "run"))
    depends_on("rocsolver@5.0:", when="+rocm", type=("build", "run"))

    depends_on("magma@2.5.0:", when="+magma @7.0:", type=("build", "run"))

    # https://github.com/spack/spack/issues/39536#issuecomment-1685161942
    conflicts("^cuda@12", when="@:7.9 +cuda")

    conflicts("+magma", when="~cuda~rocm")  # currently MAGMA only works with CUDA
    conflicts("+cuda", when="+rocm")  # can pick CUDA or ROCm, not both

    # patching a bug in the interpretation of the C++ standard
    patch("tas80_clang17.patch", when="@8.0")

    def setup_build_environment(self, env):
        # needed for the hipcc compiler
        if "+rocm" in self.spec:
            env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant("Tasmanian_ENABLE_OPENMP", "openmp"),
            self.define_from_variant("Tasmanian_ENABLE_BLAS", "blas"),
            self.define_from_variant("Tasmanian_ENABLE_PYTHON", "python"),
            self.define_from_variant("Tasmanian_ENABLE_MPI", "mpi"),
            self.define_from_variant("Tasmanian_ENABLE_CUDA", "cuda"),
            self.define_from_variant("Tasmanian_ENABLE_HIP", "rocm"),
            self.define_from_variant("Tasmanian_ENABLE_MAGMA", "magma"),
            self.define_from_variant("Tasmanian_ENABLE_FORTRAN", "fortran"),
        ]

        if spec.satisfies("+blas"):
            args.append("-DBLAS_LIBRARIES={0}".format(spec["blas"].libs.joined(";")))
            args.append("-DLAPACK_LIBRARIES={0}".format(spec["lapack"].libs.joined(";")))

        return args

    @run_after("install")
    def setup_smoke_test(self):
        install_tree(
            self.prefix.share.Tasmanian.testing, join_path(install_test_root(self), "testing")
        )

    def test_make_test(self):
        """build and run make(test)"""
        # using the tests copied from <prefix>/share/Tasmanian/testing
        cmake_dir = self.test_suite.current_test_cache_dir.testing

        options = [cmake_dir]
        if "+rocm" in self.spec:
            options.append(f"-Dhip_DIR={self.spec['hip'].prefix.lib.cmake.hip}")
            options.append(
                f"-DAMDDeviceLibs_DIR={self.spec['llvm-amdgpu'].prefix.lib.cmake.AMDDeviceLibs}"
            )
            options.append(f"-Damd_comgr_DIR={self.spec['comgr'].prefix.lib.cmake.amd_comgr}")
            options.append(
                "-Dhsa-runtime64_DIR="
                + join_path(self.spec["hsa-rocr-dev"].prefix.lib.cmake, "hsa-runtime64")
            )
            options.append(f"-DHSA_HEADER={self.spec['hsa-rocr-dev'].prefix.include}")
            options.append(f"-DCMAKE_INCLUDE_PATH={self.spec['hsa-rocr-dev'].prefix.include.hsa}")
            options.append(f"-Drocblas_DIR={self.spec['rocblas'].prefix.lib.cmake.rocblas}")
            options.append(f"-Drocsparse_DIR={self.spec['rocsparse'].prefix.lib.cmake.rocsparse}")
            options.append(f"-Drocsolver_DIR={self.spec['rocsolver'].prefix.lib.cmake.rocsolver}")

        if "+mpi" in self.spec:
            options.append("-DMPI_HOME=" + self.spec["mpi"].prefix)

        cmake = which(self.spec["cmake"].prefix.bin.cmake)
        cmake(*options)

        make = which("make")
        make()

        make("test")
