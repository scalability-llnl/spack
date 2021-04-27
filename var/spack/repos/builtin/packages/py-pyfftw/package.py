# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyfftw(PythonPackage):
    """A pythonic wrapper around FFTW, the FFT library,
    presenting a unified interface for all the supported transforms."""

    homepage = "http://hgomersall.github.com/pyFFTW"
    pypi = "pyFFTW/pyFFTW-0.10.4.tar.gz"

    version('0.12.0', sha256='60988e823ca75808a26fd79d88dbae1de3699e72a293f812aa4534f8a0a58cb0')
    version('0.11.1', sha256='05ea28dede4c3aaaf5c66f56eb0f71849d0d50f5bc0f53ca0ffa69534af14926')
    version('0.10.4', sha256='739b436b7c0aeddf99a48749380260364d2dc027cf1d5f63dafb5f50068ede1a')

    depends_on('fftw')
    depends_on('py-setuptools',        type='build')
    depends_on('py-cython@0.29:0.999', type='build')
    depends_on('py-numpy@1.6:',        type=('build', 'run'), when='@:0.10.4')
    depends_on('py-numpy@1.10:1.999',  type=('build', 'run'), when='@0.11.0:')

    def setup_build_environment(self, env):
        env.append_flags('LDFLAGS', self.spec['fftw'].libs.search_flags)
