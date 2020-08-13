# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmRocrRuntime(CMakePackage):
    """This repository includes the user-mode API interfaces and
    libraries necessary for host applications to launch compute
    kernels to available HSA ROCm kernel agents. Reference source code
    for the core runtime is also available."""

    homepage = "https://github.com/RadeonOpenCompute/ROCR-Runtime"
    url = "https://github.com/RadeonOpenCompute/ROCR-Runtime/archive/rocm-3.5.0.tar.gz"

    root_cmakelists_dir = "src"

    version('3.5.0', '52c12eec3e3404c0749c70f156229786ee0c3e6d3c979aed9bbaea500fa1f3b8')
    depends_on('rocm-roct-thunk-interface')

    @property
    def headers(self):
        headers = find_all_headers(self.prefix)
        headers.directories = [self.prefix.include]
        return headers

    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_BUILD_WITH_INSTALL_RPATH=1",
        ]
        return cmake_args
