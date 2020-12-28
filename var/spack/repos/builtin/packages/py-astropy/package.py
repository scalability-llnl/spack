# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyAstropy(PythonPackage):
    """The Astropy Project is a community effort to develop a single core
    package for Astronomy in Python and foster interoperability between
    Python astronomy packages."""

    homepage = 'https://astropy.org/'
    url = 'https://pypi.io/packages/source/a/astropy/astropy-4.0.1.post1.tar.gz'

    version('4.0.1.post1', sha256='5c304a6c1845ca426e7bc319412b0363fccb4928cb4ba59298acd1918eec44b5')
    version('3.2.1', sha256='706c0457789c78285e5464a5a336f5f0b058d646d60f4e5f5ba1f7d5bf424b28')
    version('2.0.14', sha256='618807068609a4d8aeb403a07624e9984f566adc0dc0f5d6b477c3658f31aeb6')
    version('1.1.2', sha256='6f0d84cd7dfb304bb437dda666406a1d42208c16204043bc920308ff8ffdfad1')
    version('1.1.post1', sha256='64427ec132620aeb038e4d8df94d6c30df4cc8b1c42a6d8c5b09907a31566a21')

    variant('extras', default=False, description='Enable extra functionality')

    # Required dependencies
    depends_on('python@3.6:', when='@4.0:', type=('build', 'run'))
    depends_on('python@3.5:', when='@3.0:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@2.0:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.3:', when='@1.2:', type=('build', 'run'))
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.29.13:', type='build')
    depends_on('py-numpy@1.16:', when='@4.0:', type=('build', 'run'))
    depends_on('py-numpy@1.13:', when='@3.1:', type=('build', 'run'))
    depends_on('py-numpy@1.10:', when='@3.0:', type=('build', 'run'))
    depends_on('py-numpy@1.9:', when='@2.0:', type=('build', 'run'))
    depends_on('py-numpy@1.7:', when='@1.2:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('pkgconfig', type='build')

    # Optional dependencies
    depends_on('py-scipy@0.18:', when='+extras', type=('build', 'run'))
    depends_on('py-h5py', when='+extras', type=('build', 'run'))
    depends_on('py-beautifulsoup4', when='+extras', type=('build', 'run'))
    depends_on('py-html5lib', when='+extras', type=('build', 'run'))
    depends_on('py-bleach', when='+extras', type=('build', 'run'))
    depends_on('py-pyyaml', when='+extras', type=('build', 'run'))
    depends_on('py-pandas', when='+extras', type=('build', 'run'))
    depends_on('py-bintrees', when='+extras', type=('build', 'run'))
    depends_on('py-sortedcontainers', when='+extras', type=('build', 'run'))
    depends_on('py-pytz', when='+extras', type=('build', 'run'))
    depends_on('py-jplephem', when='+extras', type=('build', 'run'))
    depends_on('py-matplotlib@2.0:', when='+extras', type=('build', 'run'))
    depends_on('py-scikit-image', when='+extras', type=('build', 'run'))
    depends_on('py-mpmath', when='+extras', type=('build', 'run'))
    depends_on('py-asdf@2.3:', when='+extras', type=('build', 'run'))
    depends_on('py-bottleneck', when='+extras', type=('build', 'run'))
    depends_on('py-pytest', when='+extras', type=('build', 'run'))

    # System dependencies
    depends_on('erfa')
    depends_on('wcslib')
    depends_on('cfitsio')
    depends_on('expat')

    def patch(self):
        # forces the rebuild of files with cython
        # avoids issues with PyCode_New() in newer
        # versions of python in the distributed
        # cython-ized files
        os.remove('astropy/cython_version.py')

    def build_args(self, spec, prefix):
        args = [
            '--use-system-libraries',
            '--use-system-erfa',
            '--use-system-wcslib',
            '--use-system-cfitsio',
            '--use-system-expat'
        ]

        if spec.satisfies('^python@3:'):
            args.extend(['-j', str(make_jobs)])

        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir('spack-test', create=True):
            python('-c', 'import astropy; astropy.test()')
