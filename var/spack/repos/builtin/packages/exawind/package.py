# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exawind(CMakePackage, CudaPackage, ROCmPackage):
    """Multi-application driver for Exawind project."""

    homepage = "https://github.com/Exawind/exawind-driver"
    git = "https://github.com/Exawind/exawind-driver.git"

    maintainers("jrood-nrel")

    tags = ["ecp", "ecp-apps"]

    license("Apache-2.0")

    version("master", branch="main", submodules=True, preferred=True)
    version("1.0.0", tag="v1.0.0", submodules=True)

    depends_on("cxx", type="build")  # generated

    variant("amr_wind_gpu", default=False, description="Enable AMR-Wind on the GPU")
    variant("nalu_wind_gpu", default=False, description="Enable Nalu-Wind on the GPU")
    variant("sycl", default=False, description="Enable SYCL backend for AMR-Wind")
    variant("gpu-aware-mpi", default=False, description="gpu-aware-mpi")

    for arch in CudaPackage.cuda_arch_values:
        depends_on(
            "amr-wind+cuda cuda_arch=%s" % arch, when="+amr_wind_gpu+cuda cuda_arch=%s" % arch
        )
        depends_on(
            "nalu-wind+cuda cuda_arch=%s" % arch, when="+nalu_wind_gpu+cuda cuda_arch=%s" % arch
        )
        depends_on(
            "trilinos+cuda cuda_arch=%s" % arch, when="+nalu_wind_gpu+cuda cuda_arch=%s" % arch
        )

    for arch in ROCmPackage.amdgpu_targets:
        depends_on(
            "amr-wind+rocm amdgpu_target=%s" % arch,
            when="+amr_wind_gpu+rocm amdgpu_target=%s" % arch,
        )
        depends_on(
            "nalu-wind+rocm amdgpu_target=%s" % arch,
            when="+nalu_wind_gpu+rocm amdgpu_target=%s" % arch,
        )
        depends_on(
            "trilinos+rocm amdgpu_target=%s" % arch,
            when="+nalu_wind_gpu+rocm amdgpu_target=%s" % arch,
        )

    depends_on("nalu-wind+hypre+fsi+openfast+tioga")
    depends_on("amr-wind+netcdf+mpi+tiny_profile")
    depends_on("trilinos")
    depends_on("yaml-cpp@0.6:")
    depends_on("tioga~nodegid")
    depends_on("openfast+cxx@2.6.0:")
    depends_on("amr-wind+sycl", when="+amr_wind_gpu+sycl")
    depends_on("kokkos-nvcc-wrapper", type="build", when="+cuda")
    depends_on("mpi")
    depends_on("nalu-wind+gpu-aware-mpi", when="+gpu-aware-mpi")
    depends_on("amr-wind+gpu-aware-mpi", when="+gpu-aware-mpi")
    depends_on("nalu-wind@2.0.0:", when="@1.0.0:")
    depends_on("amr-wind@0.9.0:", when="@1.0.0:")
    depends_on("tioga@1.0.0:", when="@1.0.0:")

    with when("~amr_wind_gpu~nalu_wind_gpu"):
        conflicts("+cuda")
        conflicts("+rocm")
        conflicts("+sycl")
    with when("~nalu_wind_gpu"):
        conflicts("^nalu-wind+cuda")
        conflicts("^nalu-wind+rocm")
    with when("~amr_wind_gpu"):
        conflicts("^amr-wind+cuda")
        conflicts("^amr-wind+rocm")
        conflicts("^amr-wind+sycl")
    conflicts("+amr_wind_gpu", when="~cuda~rocm~sycl")
    conflicts("+nalu_wind_gpu", when="~cuda~rocm")
    conflicts("+nalu_wind_gpu", when="+sycl")
    conflicts("^amr-wind+hypre", when="~amr_wind_gpu+nalu_wind_gpu")
    conflicts("^amr-wind+hypre", when="+amr_wind_gpu~nalu_wind_gpu")
    conflicts("+sycl", when="+cuda")
    conflicts("+rocm", when="+cuda")
    conflicts("+sycl", when="+rocm")

    def cmake_args(self):
        spec = self.spec

        args = [self.define("MPI_HOME", spec["mpi"].prefix)]

        if spec.satisfies("+cuda"):
            args.append(self.define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx))
            args.append(self.define("CMAKE_C_COMPILER", spec["mpi"].mpicc))
            args.append(self.define("EXAWIND_ENABLE_CUDA", True))
            args.append(self.define("CUDAToolkit_ROOT", self.spec["cuda"].prefix))
            args.append(self.define("EXAWIND_CUDA_ARCH", self.spec.variants["cuda_arch"].value))

        if spec.satisfies("+rocm"):
            targets = self.spec.variants["amdgpu_target"].value
            args.append(self.define("EXAWIND_ENABLE_ROCM", True))
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
            # Optimization to only build one specific target architecture:
            args.append(self.define("CMAKE_HIP_ARCHITECTURES", ";".join(str(x) for x in targets)))
            args.append(self.define("AMDGPU_TARGETS", ";".join(str(x) for x in targets)))
            args.append(self.define("GPU_TARGETS", ";".join(str(x) for x in targets)))

        if spec.satisfies("^amr-wind+hdf5"):
            args.append(self.define("H5Z_ZFP_USE_STATIC_LIBS", True))

        return args

    def setup_build_environment(self, env):
        env.append_flags("CXXFLAGS", "-DUSE_STK_SIMD_NONE")
        if self.spec.satisfies("+rocm+amr_wind_gpu~nalu_wind_gpu"):
            # Manually turn off device self.defines to solve Kokkos issues in Nalu-Wind headers
            env.append_flags("CXXFLAGS", "-U__HIP_DEVICE_COMPILE__ -DDESUL_HIP_RDC")
        if self.spec.satisfies("+cuda"):
            env.set("OMPI_CXX", self.spec["kokkos-nvcc-wrapper"].kokkos_cxx)
            env.set("MPICH_CXX", self.spec["kokkos-nvcc-wrapper"].kokkos_cxx)
            env.set("MPICXX_CXX", self.spec["kokkos-nvcc-wrapper"].kokkos_cxx)
        if self.spec.satisfies("+rocm"):
            env.set("OMPI_CXX", self.spec["hip"].hipcc)
            env.set("MPICH_CXX", self.spec["hip"].hipcc)
            env.set("MPICXX_CXX", self.spec["hip"].hipcc)
