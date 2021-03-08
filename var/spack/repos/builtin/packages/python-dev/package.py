# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PythonDev(BundlePackage):
    """Meta package to bundle python packages for development"""

    homepage = "http://www.dummy.org/"
    url      = "https://www.dummy.org/source/dummy-0.2.zip"

    version('0.3')

    depends_on('python', type=('build', 'run'))
    depends_on('py-beautifulsoup4', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-clustershell', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-h5py~mpi', type=('build', 'run'))
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-jinja2-cli', type=('build', 'run'))
    depends_on('py-lazy-property', type=('build', 'run'))
    depends_on('py-lxml', type=('build', 'run'))
    depends_on('py-mock', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-pyspark', type=('build', 'run'))
    depends_on('py-pytest', type=('build', 'run'))
    depends_on('py-pytest-cov', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-regex', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-simplejson', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-sympy', type=('build', 'run'))
    depends_on('py-virtualenv', type=('build', 'run'))
    depends_on('py-virtualenv-clone', type=('build', 'run'))
    depends_on('py-virtualenvwrapper', type=('build', 'run'))
    depends_on('py-wheel', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))

    def setup_run_environment(self, env):
        deps = ['py-virtualenv', 'py-wheel', 'py-cython', 'py-pyspark']
        for dep in deps:
            env.prepend_path('PATH', self.spec[dep].prefix.bin)
