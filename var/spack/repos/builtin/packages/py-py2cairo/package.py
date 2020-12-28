# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPy2cairo(WafPackage):
    """Pycairo is a set of Python bindings for the cairo graphics library."""

    homepage = "https://www.cairographics.org/pycairo/"
    url      = "https://cairographics.org/releases/py2cairo-1.10.0.tar.bz2"

    version('1.10.0', sha256='d30439f06c2ec1a39e27464c6c828b6eface3b22ee17b2de05dc409e429a7431')

    extends('python')

    depends_on('python', type=('build', 'run'))
    depends_on('cairo@1.10.0:')
    depends_on('pixman')
    depends_on('pkgconfig', type='build')

    depends_on('py-pytest', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir('test'):
            pytest = which('py.test')
            pytest()
