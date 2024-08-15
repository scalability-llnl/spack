# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Amp(CMakePackage, CudaPackage, ROCmPackage):
    """The Advanced Multi-Physics (AMP) package.

    The Advanced Multi-Physics (AMP) package is an open source parallel
    object-oriented computational framework that is designed with single
    and multi-domain multi-physics applications in mind.
    """

    homepage = "https://github.com/AdvancedMultiPhysics/AMP"
    git = "https://github.com/AdvancedMultiPhysics/AMP.git"

    maintainers("bobby-philip", "gllongo", "rbberger")

    license("UNKNOWN")

    version("master", branch="master")
    version("3.1.0", tag="3.1.0", commit="c8a52e6f3124e43ebce944ee3fae8b9a994c4dbe")

    variant("mpi", default=True, description="Build with MPI support")
    variant("hypre", default=False, description="Build with support for hypre")
    variant("kokkos", default=False, description="Build with support for Kokkos")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant("shared", default=False, description="Build shared libraries")

    depends_on("cmake@3.26.0:")
    depends_on("tpl-builder+stacktrace")

    tpl_depends = ["hypre", "kokkos", "mpi", "openmp", "cuda", "rocm", "shared"]

    for v in tpl_depends:
        depends_on(f"tpl-builder+{v}", when=f"+{v}")
        depends_on(f"tpl-builder~{v}", when=f"~{v}")

    for _flag in CudaPackage.cuda_arch_values:
        depends_on(f"tpl-builder+cuda cuda_arch={_flag}", when=f"+cuda cuda_arch={_flag}")

    for _flag in ROCmPackage.amdgpu_targets:
        depends_on(f"tpl-builder+rocm amdgpu_target={_flag}", when=f"+rocm amdgpu_target={_flag}")

    def cmake_args(self):
        spec = self.spec

        options = [
            self.define("TPL_DIRECTORY", spec["tpl-builder"].prefix),
            self.define("AMP_ENABLE_TESTS", self.run_tests),
            self.define("EXCLUDE_TESTS_FROM_ALL", not self.run_tests),
            self.define("AMP_ENABLE_EXAMPLES", False),
            self.define("CXX_STD", "17"),
        ]

        if "+rocm" in spec:
            options.append(self.define("COMPILE_CXX_AS_HIP", True))

        return options
