# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os


class RocmRocclr(CMakePackage):
    """ROCclr is a virtual device interface that compute runtimes
    interact with to different backends such as ROCr or PAL This
    abstraction allows runtimes to work on Windows as well as on Linux
    without much effort."""

    homepage = "https://github.com/ROCm-Developer-Tools/ROCclr"
    url = "https://github.com/ROCm-Developer-Tools/ROCclr/archive/roc-3.5.0.tar.gz"

    version('3.5.0', '87c1ee9f02b8aa487b628c543f058198767c474cec3d21700596a73c028959e1')
    depends_on('rocm-compilersupport')
    resource(name='ROCm-OpenCL-Runtime',
             url='https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/roc-3.5.0.tar.gz',
             sha256='511b617d5192f2d4893603c1a02402b2ac9556e9806ff09dd2a91d398abf39a0',
             destination='spack-resource-opencl')

    def cmake_args(self):
        cmake_args = [
            "-DOPENCL_DIR={0}".format(
                'spack-resource-opencl/ROCm-OpenCL-Runtime-roc-3.5.0'),
        ]
        return cmake_args

    @run_after('install')
    def install_cmake_file(self):
        with working_dir(self.build_directory):
            libfile = "libamdrocclr_static.a"
            libpath = os.path.join(self.prefix.lib, libfile)
            filter_file(r'IMPORTED_LOCATION_RELWITHDEBINFO .+',
                        'IMPORTED_LOCATION_RELWITHDEBINFO "{0}"'.format(
                            libpath),
                        "amdrocclr_staticTargets.cmake")
            install("amdrocclr_staticTargets.cmake",
                    self.prefix.lib)
