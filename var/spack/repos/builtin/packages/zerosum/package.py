# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zerosum(CMakePackage):
    """Utility for monitoring process, thread, OS and HW resources,
    including GPU utilization.
    """

    homepage = "https://github.com/UO-OACISS/zerosum"
    url = "https://github.com/UO-OACISS/zerosum.git"
    git = "https://github.com/UO-OACISS/zerosum"

    maintainers("khuck", "wspear", "sameershende")

    license("MIT", checked_by="khuck")

    version("main", branch="main")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("perfstubs", default=True, description="Enable PerfStubs support")
    variant("hwloc", default=True, description="Enable HWLOC support")
    variant("mpi", default=True, description="Enable MPI support")
    variant("cuda", default=False, description="Enable CUDA support")
    variant("hip", default=False, description="Enable HIP support")
    variant("sycl", default=False, description="Enable SYCL support")
    variant("openmp", default=True, description="Enable OpenMP support")
    # GCC has no support for OMPT, and doesn't plan to add it any time soon.
    # For that reason, we disable OMPT support by default.
    variant("ompt", default=False, when="%gcc", description="Enable OpenMP Tools support")
    # All other compilers default to having the support enabled.
    # This works because Spack allows overriding of variants:
    # "When a variant is defined multiple times, whether in the same package
    # file or in a subclass and a superclass, the _last_ definition is used
    # for all attributes except for the when clauses."
    variant("ompt", default=True, description="Enable OpenMP Tools support")

    depends_on("cmake", type="build")
    depends_on("hwloc", when="+hwloc")
    depends_on("mpi", when="+mpi")
    depends_on("rocm-smi-lib", when="+hip")
    depends_on("cuda", when="+cuda")
    depends_on("hip", when="+hip")
    depends_on("sycl", when="+sycl")

    # GCC has no support for OMPT, and doesn't plan to add it any time soon.
    # For that reason, we let the user know this support is not allowed.
    conflicts("+ompt", when="%gcc")

    conflicts("platform=darwin", msg="zerosum runs only on Linux.")
    conflicts("platform=windows", msg="zerosum runs only on Linux.")

    def cmake_args(self):
        args = [
            self.define_from_variant("ZeroSum_WITH_PerfStubs", "perfstubs"),
            self.define_from_variant("ZeroSum_WITH_HWLOC", "hwloc"),
            self.define_from_variant("ZeroSum_WITH_MPI", "mpi"),
            self.define_from_variant("ZeroSum_WITH_CUDA", "cuda"),
            self.define_from_variant("ZeroSum_WITH_HIP", "hip"),
            self.define_from_variant("ZeroSum_WITH_SYCL", "sycl"),
            self.define_from_variant("ZeroSum_WITH_OPENMP", "openmp"),
            self.define_from_variant("ZeroSum_WITH_OMPT", "ompt"),
        ]

        if "+cuda" in self.spec:
            args.append(self.define("CUDAToolkit_ROOT", self.spec["cuda"].prefix))
        if "+hip" in self.spec:
            args.append(self.define("ROCM_ROOT}", self.spec["hip"].prefix))

        return args
