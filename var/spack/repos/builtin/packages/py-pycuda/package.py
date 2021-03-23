# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPycuda(PythonPackage):
    """PyCUDA gives you easy, Pythonic access to Nvidia's CUDA parallel
    computation API
    """

    homepage = "https://mathema.tician.de/software/pycuda/"
    pypi = "pycuda/pycuda-2019.1.2.tar.gz"

    version('2020.1', sha256='effa3b99b55af67f3afba9b0d1b64b4a0add4dd6a33bdd6786df1aa4cc8761a5')
    version('2019.1.2', sha256='ada56ce98a41f9f95fe18809f38afbae473a5c62d346cfa126a2d5477f24cc8a')
    version('2016.1.2', sha256='a7dbdac7e2f0c0d2ad98f5f281d5a9d29d6673b3c20210e261b96e9a2d0b6e37')

    @run_before('build')
    def configure(self):
        pyver = self.spec['python'].version.up_to(2).joined
        boostlib = 'boost_python{0}'.format(pyver)
        configure_args = [
            '--no-use-shipped-boost',
            '--boost-inc-dir={0}'.format(self.spec['boost'].prefix.include),
            '--boost-lib-dir={0}'.format(self.spec['boost'].libs.directories[0]),
            '--boost-python-libname={0}'.format(boostlib)
        ]
        python('configure.py', *configure_args)

    depends_on('py-setuptools', type='build')
    depends_on('cuda')
    depends_on('boost+python')
    depends_on('python@3.6:3.999', type=('build', 'run'), when='@2020.1:')
    depends_on('py-numpy@1.6:', type=('build', 'run'))
    depends_on('py-pytools@2011.2:', type=('build', 'run'))
    depends_on('py-six', type='run')
    depends_on('py-decorator@3.2.0:', type=('build', 'run'))
    depends_on('py-appdirs@1.4.0:', type=('build', 'run'))
    depends_on('py-mako', type=('build', 'run'))

    depends_on('cuda@:8.0.61', when='@2016.1.2')
