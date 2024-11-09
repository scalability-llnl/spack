# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Camp(CMakePackage, CudaPackage, ROCmPackage):
    """
    Compiler agnostic metaprogramming library providing concepts,
    type operations and tuples for C++ and cuda
    """

    homepage = "https://github.com/LLNL/camp"
    git = "https://github.com/LLNL/camp.git"
    url = "https://github.com/LLNL/camp/archive/v0.1.0.tar.gz"

    maintainers("trws", "adrienbernede")

    license("BSD-3-Clause")

    version("main", branch="main", submodules=False)
    version(
        "2024.07.0",
        tag="v2024.07.0",
        commit="0f07de4240c42e0b38a8d872a20440cb4b33d9f5",
        submodules=False,
    )
    version(
        "2024.02.1",
        tag="v2024.02.1",
        commit="79c320fa09db987923b56884afdc9f82f4b70fc4",
        submodules=False,
    )
    version(
        "2024.02.0",
        tag="v2024.02.0",
        commit="03c80a6c6ab4f97e76a52639563daec71435a277",
        submodules=False,
    )
    version(
        "2023.06.0",
        tag="v2023.06.0",
        commit="ac34c25b722a06b138bc045d38bfa5e8fa3ec9c5",
        submodules=False,
    )
    version("2022.10.1", sha256="2d12f1a46f5a6d01880fc075cfbd332e2cf296816a7c1aa12d4ee5644d386f02")
    version("2022.10.0", sha256="3561c3ef00bbcb61fe3183c53d49b110e54910f47e7fc689ad9ccce57e55d6b8")
    version("2022.03.2", sha256="bc4aaeacfe8f2912e28f7a36fc731ab9e481bee15f2c6daf0cb208eed3f201eb")
    version("2022.03.0", sha256="e9090d5ee191ea3a8e36b47a8fe78f3ac95d51804f1d986d931e85b8f8dad721")
    version("0.3.0", sha256="129431a049ca5825443038ad5a37a86ba6d09b2618d5fe65d35f83136575afdb")
    version("0.2.3", sha256="58a0f3bd5eadb588d7dc83f3d050aff8c8db639fc89e8d6553f9ce34fc2421a7")
    version("0.2.2", sha256="194d38b57e50e3494482a7f94940b27f37a2bee8291f2574d64db342b981d819")
    version("0.1.0", sha256="fd4f0f2a60b82a12a1d9f943f8893dc6fe770db493f8fae5ef6f7d0c439bebcc")

    depends_on("cxx", type="build")  # generated

    # TODO: figure out gtest dependency and then set this default True.
    variant("tests", default=False, description="Build tests")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant("omptarget", default=False, description="Build with OpenMP Target support")
    variant("sycl", default=False, description="Build with Sycl support")

    depends_on("cub", when="+cuda")

    depends_on("blt", type="build")
    depends_on("blt@0.6.2:", type="build", when="@2024.02.1:")
    depends_on("blt@0.6.1", type="build", when="@2024.02.0")
    depends_on("blt@0.5.0:0.5.3", type="build", when="@2022.03.0:2023.06.0")

    patch("libstdc++-13-missing-header.patch", when="@:2022.10")

    patch("camp-rocm6.patch", when="@0.2.3 +rocm ^hip@6:")

    conflicts("^blt@:0.3.6", when="+rocm")

    conflicts("+omptarget +rocm")
    conflicts("+sycl +omptarget")
    conflicts("+sycl +rocm")
    conflicts(
        "+sycl",
        when="@:2024.02.99",
        msg="Support for SYCL was introduced in RAJA after 2024.02 release, "
        "please use a newer release.",
    )

    def cmake_args(self):
        spec = self.spec

        options = []

        options.append("-DBLT_SOURCE_DIR={0}".format(spec["blt"].prefix))

        options.append(self.define_from_variant("ENABLE_CUDA", "cuda"))
        if spec.satisfies("+cuda"):
            options.append("-DCUDA_TOOLKIT_ROOT_DIR={0}".format(spec["cuda"].prefix))

            if not spec.satisfies("cuda_arch=none"):
                cuda_arch = spec.variants["cuda_arch"].value
                options.append("-DCMAKE_CUDA_ARCHITECTURES={0}".format(cuda_arch[0]))
                options.append("-DCUDA_ARCH=sm_{0}".format(cuda_arch[0]))
                flag = "-arch sm_{0}".format(cuda_arch[0])
                options.append("-DCMAKE_CUDA_FLAGS:STRING={0}".format(flag))

        options.append(self.define_from_variant("ENABLE_HIP", "rocm"))
        if spec.satisfies("+rocm"):
            options.append("-DHIP_ROOT_DIR={0}".format(spec["hip"].prefix))

            archs = self.spec.variants["amdgpu_target"].value
            options.append("-DCMAKE_HIP_ARCHITECTURES={0}".format(archs))
            options.append("-DGPU_TARGETS={0}".format(archs))
            options.append("-DAMDGPU_TARGETS={0}".format(archs))

        if spec.satisfies("+omptarget"):
            options.append(cmake_cache_string("RAJA_DATA_ALIGN", 64))

        options.append(self.define_from_variant("ENABLE_TESTS", "tests"))
        options.append(self.define_from_variant("ENABLE_OPENMP", "openmp"))
        options.append(self.define_from_variant("CAMP_ENABLE_TARGET_OPENMP", "omptarget"))
        options.append(self.define_from_variant("ENABLE_SYCL", "sycl"))

        return options
