# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Aluminum(CMakePackage, CudaPackage, ROCmPackage):
    """Aluminum provides a generic interface to high-performance
    communication libraries, with a focus on allreduce
    algorithms. Blocking and non-blocking algorithms and GPU-aware
    algorithms are supported. Aluminum also contains custom
    implementations of select algorithms to optimize for certain
    situations."""

    homepage = "https://github.com/LLNL/Aluminum"
    url      = "https://github.com/LLNL/Aluminum/archive/v0.1.tar.gz"
    git      = "https://github.com/LLNL/Aluminum.git"

    maintainers = ['bvanessen']

    version('master', branch='master')
    version('1.0.0', sha256='028d12e271817214db5c07c77b0528f88862139c3e442e1b12f58717290f414a')
    version('0.7.0', sha256='bbb73d2847c56efbe6f99e46b41d837763938483f2e2d1982ccf8350d1148caa')
    version('0.6.0', sha256='6ca329951f4c7ea52670e46e5020e7e7879d9b56fed5ff8c5df6e624b313e925')
    version('0.5.0', sha256='dc365a5849eaba925355a8efb27005c5f22bcd1dca94aaed8d0d29c265c064c1')
    version('0.4.0', sha256='4d6fab5481cc7c994b32fb23a37e9ee44041a9f91acf78f981a97cb8ef57bb7d')
    version('0.3.3',   sha256='26e7f263f53c6c6ee0fe216e981a558dfdd7ec997d0dd2a24285a609a6c68f3b')
    version('0.3.2',   sha256='09b6d1bcc02ac54ba269b1123eee7be20f0104b93596956c014b794ba96b037f')
    version('0.2.1-1', sha256='066b750e9d1134871709a3e2414b96b166e0e24773efc7d512df2f1d96ee8eef')
    version('0.2.1', sha256='3d5d15853cccc718f60df68205e56a2831de65be4d96e7f7e8497097e7905f89')
    version('0.2', sha256='fc8f06c6d8faab17a2aedd408d3fe924043bf857da1094d5553f35c4d2af893b')
    version('0.1', sha256='3880b736866e439dd94e6a61eeeb5bb2abccebbac82b82d52033bc6c94950bdb')

    variant('nccl', default=False, description='Builds with support for NCCL communication lib')
    variant('ht', default=False, description='Builds with support for host-enabled MPI'
            ' communication of accelerator data')
    variant('cuda_rma', default=False, description='Builds with support for CUDA intra-node '
            ' Put/Get and IPC RMA functionality')
    variant('rccl', default=False, description='Builds with support for NCCL communication lib')

    depends_on('cmake@3.17.0:', type='build')
    depends_on('mpi')
    depends_on('nccl@2.7.0-0:', when='+nccl')
    depends_on('hwloc@1.11:')
    depends_on('hwloc +cuda +nvml', when='+cuda')
    depends_on('hwloc@2.3.0:', when='+rocm')
    depends_on('cub', when='@:0.1,0.6.0: +cuda ^cuda@:10.99')
    depends_on('hipcub', when='@:0.1,0.6.0: +rocm')

    conflicts('~cuda', when='+cuda_rma', msg='CUDA RMA support requires CUDA')
    conflicts('+cuda', when='+rocm', msg='CUDA and ROCm support are mutually exclusive')

    generator = 'Ninja'
    depends_on('ninja', type='build')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DCMAKE_CXX_STANDARD=14',
            '-DALUMINUM_ENABLE_CUDA:BOOL=%s' % ('+cuda' in spec),
            '-DALUMINUM_ENABLE_NCCL:BOOL=%s' % ('+nccl' in spec or '+rccl' in spec),
            '-DALUMINUM_ENABLE_ROCM:BOOL=%s' % ('+rocm' in spec)]

        if '+cuda' in spec:
            args.append('-DCMAKE_CUDA_STANDARD=14')

        if spec.satisfies('@0.5:'):
            args.extend([
                '-DALUMINUM_ENABLE_HOST_TRANSFER:BOOL=%s' % ('+ht' in spec),
                '-DALUMINUM_ENABLE_MPI_CUDA:BOOL=%s' %
                ('+cuda_rma' in spec),
                '-DALUMINUM_ENABLE_MPI_CUDA_RMA:BOOL=%s' %
                ('+cuda_rma' in spec)])
        else:
            args.append(
                '-DALUMINUM_ENABLE_MPI_CUDA:BOOL=%s' % ('+ht' in spec))

        if spec.satisfies('@:0.1,0.6.0: +cuda ^cuda@:10.99'):
            args.append(
                '-DCUB_DIR:FILEPATH=%s' % spec['cub'].prefix)

        # Add support for OS X to find OpenMP (LLVM installed via brew)
        if self.spec.satisfies('%clang platform=darwin'):
            clang = self.compiler.cc
            clang_bin = os.path.dirname(clang)
            clang_root = os.path.dirname(clang_bin)
            args.extend([
                '-DOpenMP_DIR={0}'.format(clang_root)])

        if '+rocm' in spec:
            args.extend([
                '-DHIP_ROOT_DIR={0}'.format(spec['hip'].prefix),
                '-DHIP_CXX_COMPILER={0}'.format(self.spec['hip'].hipcc)])
            archs = self.spec.variants['amdgpu_target'].value
            if archs != 'none':
                arch_str = ",".join(archs)
                args.append(
                    '-DHIP_HIPCC_FLAGS=--amdgpu-target={0}'
                    ' -g -fsized-deallocation -fPIC'.format(arch_str)
                )

        return args
