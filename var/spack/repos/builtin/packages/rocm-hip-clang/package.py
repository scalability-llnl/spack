# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmHipClang(CMakePackage):
    """HIP-Clang: llvm and clang for ROCm"""

    homepage = "https://github.com/RadeonOpenCompute/llvm-project"
    url = "https://github.com/RadeonOpenCompute/llvm-project/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', '4878fa85473b24d88edcc89938441edc85d2e8a785e567b7bd7ce274ecc2fd9c')
    depends_on('gcc')

    root_cmakelists_dir = "llvm"

    def cmake_args(self):
        spec = self.spec
        cmake_args = [
            "-DLLVM_ENABLE_PROJECTS=clang;lld",
            "-DLLVM_TARGETS_TO_BUILD=AMDGPU;X86",
            "-DGCC_INSTALL_PREFIX={0}".format(spec["gcc"].prefix),
        ]
        return cmake_args
