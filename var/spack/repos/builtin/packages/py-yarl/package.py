# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyYarl(PythonPackage):
    """The module provides handy URL class for URL parsing and changing."""

    homepage = "https://github.com/aio-libs/yarl"
    url      = "https://github.com/aio-libs/yarl/archive/v1.4.2.tar.gz"

    version('1.4.2', sha256='a400eb3f54f7596eeaba8100a8fa3d72135195423c52808dc54a43c6b100b192')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-multidict@4.0:', type=('build', 'run'))
    depends_on('py-idna@2.0:', type=('build', 'run'))

    @run_before('build')
    def fix_cython(self):
        cython = self.spec['py-cython'].command
        cython('-3',
               '-o',
               'yarl/_quoting.c',
               'yarl/_quoting.pyx',
               '-Iyarl')
