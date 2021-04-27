# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

from spack.pkgkit import *


class Nvshmem(MakefilePackage, CudaPackage):
    """NVSHMEM is a parallel programming interface based on OpenSHMEM that
    provides efficient and scalable communication for NVIDIA GPU
    clusters. NVSHMEM creates a global address space for data that spans
    the memory of multiple GPUs and can be accessed with fine-grained
    GPU-initiated operations, CPU-initiated operations, and operations on
    CUDA streams."""

    homepage = "https://developer.nvidia.com/nvshmem"
    url      = "https://developer.nvidia.com/nvshmem-src-203-0"

    maintainers = ['bvanessen']

    version('2.0.3-0', sha256='20da93e8508511e21aaab1863cb4c372a3bec02307b932144a7d757ea5a1bad2', extension='txz')

    variant('cuda', default=True, description='Build with CUDA')
    conflicts('~cuda')

    def url_for_version(self, version):
        ver_str = '{0}'.format(version)
        ver = re.sub('[.]', '', ver_str)
        url_fmt = "https://developer.nvidia.com/nvshmem-src-{0}"
        return url_fmt.format(ver)

    depends_on('mpi')
    depends_on('gdrcopy')

    def setup_build_environment(self, env):
        env.append_flags(
            'NVSHMEM_PREFIX', self.prefix)
        env.append_flags(
            'NVSHMEM_MPI_SUPPORT', '1')
        env.append_flags(
            'NVSHMEM_USE_GDRCOPY', '1')

        if self.spec.satisfies('^spectrum-mpi') or self.spec.satisfies('^openmpi'):
            env.append_flags(
                'NVSHMEM_MPI_IS_OMPI', '1')
            env.append_flags(
                'NVSHMEM_SHMEM_SUPPORT', '1')
        else:
            env.append_flags(
                'NVSHMEM_MPI_IS_OMPI', '0')
            env.append_flags(
                'NVSHMEM_SHMEM_SUPPORT', '0')
