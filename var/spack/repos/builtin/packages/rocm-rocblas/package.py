# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmRocblas(CMakePackage):
    """rocBLAS is AMD's library for BLAS on ROCm. It is implemented in
    the HIP programming language and optimized for AMD's GPUs."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocBLAS"
    url = "https://github.com/ROCmSoftwarePlatform/rocBLAS/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', '3e372c7c0504c0f18b5e69989083e68a45131e675912082961a736cb3b1222fb')
    depends_on('rocm-hip-clang')
    depends_on('rocm-hip')
    depends_on('rocm-cmake')
    depends_on('python@3:', type='build')
    depends_on('py-pyyaml', type='build')
    depends_on('py-msgpack', type='build')

    resource(name='ROCm-Tensile',
             url='https://github.com/ROCmSoftwarePlatform/Tensile/archive/rocm-3.5.0.tar.gz',
             sha256='1afd2e28065849dc418efdc79fc3216208963cabc0c4efb870440b1c051a0f20',
             destination='spack-resource-tensile')

    def patch(self):
        filter_file(r'HCC=.*',
                    'HCC=hipcc',
                    'header_compilation_tests.sh')
        filter_file(r'\-hc ',
                    '',
                    'header_compilation_tests.sh')
        file_to_patch = ('spack-resource-tensile/Tensile-rocm-3.5.0/'
                         'Tensile/Source/lib/include/Tensile/llvm/YAML.hpp')
        filter_file(r'Impl::inputOne\(io, key, \*value\);',
                    'Impl::inputOne(io, key.str(), *value);',
                    file_to_patch)

    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_CXX_COMPILER=hipcc",
            "-DTensile_TEST_LOCAL_PATH={0}".format(
                join_path(self.stage.source_path,
                          'spack-resource-tensile/Tensile-rocm-3.5.0')),
            "-DTensile_COMPILER=hipcc",
        ]
        return cmake_args
