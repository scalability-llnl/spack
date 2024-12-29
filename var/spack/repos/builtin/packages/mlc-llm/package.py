# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class MlcLlm(CMakePackage, CudaPackage):
    """MLC LLM is a machine learning compiler and high-performance deployment
    engine for large language models. The mission of this project is to enable
    everyone to develop, optimize, and deploy AI models natively on everyone's
    platforms."""

    homepage = "https://github.com/mlc-ai/mlc-llm"
    git = "https://github.com/mlc-ai/mlc-llm.git"
    url = "https://github.com/mlc-ai/mlc-llm/archive/refs/tags/v0.1.dev0.tar.gz"

    license("Apache-2.0", checked_by="alex391")

    version("2024-06-13", commit="ceba9511df3da06a8541916522d57fdc99cb6f54", submodules=True)

    depends_on("cmake@3.24:", type="build")
    depends_on("rust", type="build")
    depends_on("cxx", type="build")
    depends_on("python@3.11", type="build")
    depends_on("apache-tvm")

    depends_on("cuda@11.8:", when="+cuda")

    variant(
        "flash-infer",
        default=False,
        description="Use FlashInfer? (need CUDA w/ compute capability 80;86;89;90)",
        when="+cuda",
    )
    conflicts("cuda_arch=none", when="+flash-infer")

    unsupported_flash_infer_cuda_archs = filter(
        lambda arch: arch not in ["80", "86", "89", "90"], CudaPackage.cuda_arch_values
    )
    for arch in unsupported_flash_infer_cuda_archs:
        conflicts(
            f"cuda_arch={arch}",
            when="+flash-infer",
            msg=f"CUDA architecture {arch} is not supported when +flash-infer",
        )

    def patch(self):
        with open("cmake/config.cmake", "w") as f:
            f.write(self._gen_cmake_config())

    def _gen_cmake_config(self) -> str:
        """
        Generate string for cmake/config.cmake (based on cmake/gen_cmake_config.py)
        """

        tvm_home = self.spec["apache-tvm"].prefix

        cmake_config_str = f"set(TVM_SOURCE_DIR {tvm_home})\n"
        cmake_config_str += "set(CMAKE_BUILD_TYPE RelWithDebInfo)\n"

        if self.spec.satisfies("+cuda"):
            cmake_config_str += "set(USE_CUDA ON)\n"
            cmake_config_str += "set(USE_THRUST ON)\n"
        else:
            cmake_config_str += "set(USE_CUDA OFF)\n"

        # FlashInfer related
        if self.spec.satisfies("+flash-infer"):
            cmake_config_str += "set(USE_FLASHINFER ON)\n"
            cmake_config_str += "set(FLASHINFER_ENABLE_FP8 OFF)\n"
            cmake_config_str += "set(FLASHINFER_ENABLE_BF16 OFF)\n"
            cmake_config_str += "set(FLASHINFER_GEN_GROUP_SIZES 1 4 6 8)\n"
            cmake_config_str += "set(FLASHINFER_GEN_PAGE_SIZES 16)\n"
            cmake_config_str += "set(FLASHINFER_GEN_HEAD_DIMS 128)\n"
            cmake_config_str += "set(FLASHINFER_GEN_KV_LAYOUTS 0 1)\n"
            cmake_config_str += "set(FLASHINFER_GEN_POS_ENCODING_MODES 0 1)\n"
            cmake_config_str += 'set(FLASHINFER_GEN_ALLOW_FP16_QK_REDUCTIONS "false")\n'
            cmake_config_str += 'set(FLASHINFER_GEN_CASUALS "false" "true")\n'

            cuda_archs = ";".join(self.spec.variants["cuda_arch"].value)
            cmake_config_str += f"set(FLASHINFER_CUDA_ARCHITECTURES {cuda_archs})\n"
            cmake_config_str += f"set(CMAKE_CUDA_ARCHITECTURES {cuda_archs})\n"
        else:
            cmake_config_str += "set(USE_FLASHINFER OFF)\n"

        return cmake_config_str
