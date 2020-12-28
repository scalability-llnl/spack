# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyGpustat(PythonPackage):
    """An utility to monitor NVIDIA GPU status and usage."""

    homepage = "https://github.com/wookayin/gpustat"
    url      = "https://pypi.io/packages/source/g/gpustat/gpustat-0.6.0.tar.gz"

    version('0.6.0', sha256='f69135080b2668b662822633312c2180002c10111597af9631bb02e042755b6c')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('py-six@1.7:', type=('build', 'run'))
    depends_on('py-nvidia-ml-py@7.352.0:', when='^python@:2', type=('build', 'run'))
    depends_on('py-nvidia-ml-py3@7.352.0:', when='^python@3:', type=('build', 'run'))
    depends_on('py-psutil', type=('build', 'run'))
    depends_on('py-blessings@1.6:', type=('build', 'run'))
