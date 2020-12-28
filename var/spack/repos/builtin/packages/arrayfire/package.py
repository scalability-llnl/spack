# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Arrayfire(CMakePackage, CudaPackage):
    """ArrayFire is a high performance software library for parallel computing
    with an easy-to-use API. Its array based function set makes parallel
    programming more accessible."""

    homepage = "http://arrayfire.org/docs/index.htm"
    git      = "https://github.com/arrayfire/arrayfire.git"

    version('master', submodules=True)
    version('3.7.0', submodules=True, tag='v3.7.0')

    variant('cuda',   default=False, description='Enable Cuda backend')
    variant('forge',   default=False, description='Enable graphics library')
    variant('opencl', default=False, description='Enable OpenCL backend')

    depends_on('boost@1.65:')
    depends_on('fftw')
    depends_on('blas')
    depends_on('cuda@7.5:', when='+cuda')
    depends_on('cudnn', when='+cuda')
    depends_on('opencl +icd', when='+opencl')
    # TODO add more opencl backends:
    # currently only Cuda backend is enabled
    # https://github.com/arrayfire/arrayfire/wiki/Build-Instructions-for-Linux#opencl-backend-dependencies

    depends_on('fontconfig', when='+forge')
    depends_on('glfw@3.1.4:', when='+forge')

    def cmake_args(self):
        args = []
        args.extend([
            '-DAF_BUILD_CUDA={0}'.format(
                'ON' if '+cuda' in self.spec else 'OFF'),
            '-DAF_BUILD_FORGE={0}'.format(
                'ON' if '+forge' in self.spec else 'OFF'),
            '-DAF_BUILD_OPENCL={0}'.format(
                'ON' if '+opencl' in self.spec else 'OFF'),
        ])
        return args
