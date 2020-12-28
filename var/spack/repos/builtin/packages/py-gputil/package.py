# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGputil(PythonPackage):
    """GPUtil is a Python module for getting the GPU status from NVIDA GPUs
    using nvidia-smi."""

    homepage = "https://github.com/anderskm/gputil"
    url      = "https://pypi.io/packages/source/G/GPUtil/GPUtil-1.4.0.tar.gz"

    version('1.4.0', sha256='099e52c65e512cdfa8c8763fca67f5a5c2afb63469602d5dcb4d296b3661efb9')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')

    def install(self, spec, prefix):
        # Override install to avoid
        #   error: option --single-version-externally-managed not recognized
        setup_py('install', '--root=/', '--prefix={0}'.format(prefix))
