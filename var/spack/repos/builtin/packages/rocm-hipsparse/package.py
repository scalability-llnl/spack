# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmHipsparse(CMakePackage):
    """hipSPARSE is a SPARSE marshalling library, with multiple
    supported backends. It sits between the application and a 'worker'
    SPARSE library, marshalling inputs into the backend library and
    marshalling results back to the application. hipSPARSE exports an
    interface that does not require the client to change, regardless
    of the chosen backend. Currently, hipSPARSE supports rocSPARSE and
    cuSPARSE as backends."""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipSPARSE"
    url = "https://github.com/ROCmSoftwarePlatform/hipSPARSE/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', 'fa16b2a307a5d9716066c2876febcbc1cef855bf0c96d235d2d8f2206a0fb69d')
    depends_on('rocm-hip-clang')
    depends_on('rocm-hip')
    depends_on('rocm-cmake')
    depends_on('rocm-rocsparse')

    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_CXX_COMPILER=hipcc",
        ]
        return cmake_args
