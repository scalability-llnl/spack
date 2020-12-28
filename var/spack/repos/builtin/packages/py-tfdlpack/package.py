# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyTfdlpack(CMakePackage):
    """Tensorflow plugin for DLPack."""

    homepage = "https://github.com/VoVAllen/tf-dlpack"
    git      = "https://github.com/VoVAllen/tf-dlpack.git"

    maintainers = ['adamjstewart']

    version('master', branch='master', submodules=True)
    version('0.1.1', tag='v0.1.1', submodules=True)

    variant('cuda', default=True, description='Build with CUDA support')

    depends_on('cmake@3.5:', type='build')
    depends_on('cuda', when='+cuda')

    # Python dependencies
    extends('python')
    depends_on('py-setuptools', type='build')
    depends_on('py-tensorflow', type=('build', 'run'))

    def cmake_args(self):
        args = ['-DPYTHON_EXECUTABLE=' + self.spec['python'].command.path]

        if '+cuda' in self.spec:
            args.append('-DUSE_CUDA=ON')
        else:
            args.append('-DUSE_CUDA=OFF')

        return args

    def install(self, spec, prefix):
        with working_dir('python'):
            setup_py('install', '--prefix=' + prefix,
                     '--single-version-externally-managed', '--root=/')

    def setup_run_environment(self, env):
        # Prevent TensorFlow from taking over the whole GPU
        env.set('TF_FORCE_GPU_ALLOW_GROWTH', 'true')
