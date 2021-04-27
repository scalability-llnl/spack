# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os


class Openmm(CMakePackage, CudaPackage):
    """A high performance toolkit for molecular simulation. Use it as
    a library, or as an application. We include extensive language
    bindings for Python, C, C++, and even Fortran. The code is open
    source and actively maintained on Github, licensed under MIT and
    LGPL. Part of the Omnia suite of tools for predictive biomolecular
    simulation. """

    homepage = "http://openmm.org/"
    url      = "https://github.com/openmm/openmm/archive/7.4.1.tar.gz"

    version('7.5.0', sha256='516748b4f1ae936c4d70cc6401174fc9384244c65cd3aef27bc2c53eac6d6de5')
    version('7.4.1', sha256='e8102b68133e6dcf7fcf29bc76a11ea54f30af71d8a7705aec0aee957ebe3a6d')

    install_targets = ['install', 'PythonInstall']

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('cmake@3.1:', type='build')
    depends_on('doxygen', type='build')
    depends_on('swig', type='build')
    depends_on('fftw')
    depends_on('py-cython', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('cuda', when='+cuda', type=('build', 'link', 'run'))
    extends('python')

    def patch(self):
        install_string = "set(PYTHON_SETUP_COMMAND \"install " \
                         "--prefix={0}\")".format(self.prefix)

        filter_file(r'set\(PYTHON_SETUP_COMMAND \"install.*',
                    install_string,
                    'wrappers/python/CMakeLists.txt')

    def setup_run_environment(self, env):
        spec = self.spec
        if '+cuda' in spec:
            env.set('OPENMM_CUDA_COMPILER',
                    self.spec['cuda'].prefix.bin.nvcc)
            env.prepend_path('PATH',
                             os.path.dirname(self.compiler.cc))
