# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Resolve(CMakePackage, CudaPackage, ROCmPackage):
    """ReSolve is a library of GPU-resident sparse linear solvers. It contains iterative and direct
    solvers designed to run on NVIDIA and AMD GPUs, as well as CPU devices."""

    homepage = "https://github.com/ORNL/ReSolve"
    git = "https://github.com/ORNL/ReSolve.git"

    maintainers("cameronrutherford", "pelesh", "ryandanehy", "kswirydo")

    version(
        "0.99.1",
        submodules=False,
        tag="v0.99.1",
        commit="e10dd417e836f47b3dc7c8b123a81bfbb654ee82",
    )
    version("develop", submodules=False, branch="develop")

    depends_on("cxx", type="build")  # generated

    variant("klu", default=True, description="Use KLU, AMD and COLAMD Libraries from SuiteSparse")
    variant(
        "lusol",
        default=True,
        when="@develop:",
        description="Build the LUSOL Library. Requires fortran",
    )

    depends_on("suite-sparse", when="+klu")

    with when("+rocm"):
        # Need at least 5.6+
        depends_on("rocsparse@5.6:")
        depends_on("rocblas@5.6:")
        depends_on("rocsolver@5.6:")

        # Optional profiling dependecies
        # Will be controlled by variant in the future
        # depends_on("roctracer-dev@5.6:")
        # depends_on("roctracer-dev-api@5.6:")
        # depends_on("rocprofiler-dev@5.6:")

    def cmake_args(self):
        args = []
        spec = self.spec

        args.extend(
            [
                self.define_from_variant("RESOLVE_USE_KLU", "klu"),
                self.define_from_variant("RESOLVE_USE_LUSOL", "lusol"),
                self.define("RESOLVE_TEST_WITH_BSUB", False),
            ]
        )

        if "+cuda" in spec:
            cuda_arch_list = spec.variants["cuda_arch"].value
            if cuda_arch_list[0] != "none":
                args.append(self.define("CMAKE_CUDA_ARCHITECTURES", cuda_arch_list))
            else:
                args.append(self.define("CMAKE_CUDA_ARCHITECTURES", "70;75;80"))
            args.append(self.define("RESOLVE_USE_CUDA", True))

        elif "+rocm" in spec:
            rocm_arch_list = spec.variants["amdgpu_target"].value
            # `+rocm` conflicts with amdgpu_target == "none"...
            # if rocm_arch_list[0] == "none":
            #     rocm_arch_list = "gfx90a"
            args.append(self.define("GPU_TARGETS", rocm_arch_list))
            args.append(self.define("AMDGPU_TARGETS", rocm_arch_list))
            args.append(self.define("RESOLVE_USE_HIP", True))

        return args
