# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Beatnik(CMakePackage, CudaPackage, ROCmPackage):
    """Fluid interface model solver and benchmark to test global communication strategies based on Pandya and Shkoller's Z-Model formulation."""

    homepage = "https://github.com/CUP-ECS/beatnik"
    git = "https://github.com/CUP-ECS/beatnik.git"

    maintainers("patrickb314", "JStewart28")

    # Add proper versions and checksums here. Will add 1.0 when a proper SHA is available
    # version("1.0", sha256="XXX")
    version("develop", branch="develop")
    version("main", branch="main")

    # Variants are primarily backends to build on GPU systems and pass the right
    # informtion to the packages we depend on
    variant("cuda", default=False, description="Use CUDA support from subpackages")
    variant("openmp", default=False, description="Use OpenMP support from subpackages")

    # Dependencies for all Beatnik versions
    depends_on("blt", type='build')
    depends_on("mpi")

    # Kokkos dependencies
    depends_on("kokkos @4:")
    depends_on("kokkos +cuda +cuda_lambda +cuda_constexpr", when="+cuda")
    depends_on("kokkos +rocm", when="+rocm")
    depends_on("kokkos +wrapper", when="%gcc+cuda") # XXX figure out what other compilers need the wrapper

    # Cabana dependencies
    depends_on("cabana +cajita +heffte +silo +mpi")
    depends_on("cabana @0.5.0", when="@main")
    depends_on("cabana @0.6.0", when="@1.0")
    depends_on("cabana @master", when="@develop")
    depends_on("cabana +cuda", when="+cuda")
    depends_on("cabana +rocm", when="+rocm")

    # Silo dependencies
    depends_on("silo @4.11:")

    # Heffte dependencies
    depends_on("heffte +fftw") # We make heffte explicit so we can propagate the right 
                               # cuda/rocm flags to it. Cabana currently may not. We also
                               # always require FFTW so that there's a host backend even
                               # when we're compiling for GPUs
    depends_on("heffte +cuda", when="+cuda")
    depends_on("heffte +rocm", when="+rocm")

    # If we're using CUDA or ROCM, require MPIs be GPU-aware
    conflicts("mpich ~cuda", when="+cuda")
    conflicts("mpich ~rocm", when="+rocm")
    conflicts("openmpi ~cuda", when="+cuda")
    conflicts("^intel-mpi") # Heffte won't build with intel MPI because of needed C++ MPI support

    # Propagate CUDA and AMD GPU targets to the submodules that need them
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            "kokkos cuda_arch=%s" % cuda_arch,
            when="+cuda cuda_arch=%s" % cuda_arch,
        )
        depends_on(
            "heffte +cuda cuda_arch=%s" % cuda_arch,
            when="+cuda cuda_arch=%s" % cuda_arch,
        )
    for amdgpu_value in ROCmPackage.amdgpu_targets:
        depends_on(
            "kokkos amdgpu_target=%s" % amdgpu_value,
            when="+rocm amdgpu_target=%s" % amdgpu_value,
        )
        depends_on(
            "cabana amdgpu_target=%s" % amdgpu_value,
            when="+rocm amdgpu_target=%s" % amdgpu_value,
        )
        depends_on(
            "heffte amdgpu_target=%s" % amdgpu_value,
            when="+rocm amdgpu_target=%s" % amdgpu_value,
        )

    # CMake specific build functions
    def cmake_args(self):
        args = []

        if "+rocm" in self.spec:
            args.append("-DCMAKE_CXX_COMPILER={0}".format(self.spec["hip"].hipcc))

            rocm_arch = self.spec.variants["amdgpu_target"].value
            if "none" not in rocm_arch:
                args.append("-DCMAKE_CXX_FLAGS={0}".format(self.hip_flags(rocm_arch)))

            # See https://github.com/ROCmSoftwarePlatform/rocFFT/issues/322
            if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
                args.append(self.define("__skip_rocmclang", "ON"))

        # Pull BLT from teh spack spec so we don't need the submodule
        args.append("-DBLT_SOURCE_DIR:PATH={0}".format(self.spec["blt"].prefix))

        return args
