# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCupy(PythonPackage):
    """CuPy is an open-source array library accelerated with
    NVIDIA CUDA. CuPy provides GPU accelerated computing with
    Python. CuPy uses CUDA-related libraries including cuBLAS,
    cuDNN, cuRand, cuSolver, cuSPARSE, cuFFT and NCCL to make
    full use of the GPU architecture."""

    homepage = "https://cupy.dev/"
    url = "https://pypi.io/packages/source/c/cupy/cupy-8.0.0.tar.gz"

    version('8.0.0', sha256='d1dcba5070dfa754445d010cdc952ff6b646d5f9bdcd7a63e8246e2472c3ddb8')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-fastrlock@0.3:', type=('build', 'run'))
    depends_on('py-numpy@1.15:', type=('build', 'run'))
    depends_on('cuda')
    depends_on('nccl')
    depends_on('cudnn')
