# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyCffi(PythonPackage):
    """Foreign Function Interface for Python calling C code"""

    homepage = "https://cffi.readthedocs.io/en/latest/"
    url      = "https://pypi.io/packages/source/c/cffi/cffi-1.13.0.tar.gz"

    version('1.14.3', sha256='f92f789e4f9241cd262ad7a555ca2c648a98178a953af117ef7fad46aa1d5591')
    version('1.13.0', sha256='8fe230f612c18af1df6f348d02d682fe2c28ca0a6c3856c99599cdacae7cf226')
    version('1.12.2', sha256='e113878a446c6228669144ae8a56e268c91b7f1fafae927adc4879d9849e0ea7')
    version('1.11.5', sha256='e90f17980e6ab0f3c2f3730e56d1fe9bcba1891eeea58966e89d352492cc74f4')
    version('1.10.0', sha256='b3b02911eb1f6ada203b0763ba924234629b51586f72a21faacc638269f4ced5')
    version('1.1.2',  sha256='390970b602708c91ddc73953bb6929e56291c18a4d80f360afa00fad8b6f3339')

    depends_on('pkgconfig', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-pycparser', type=('build', 'run'))
    depends_on('py-pycparser@2.19:', when='^python@:2.6', type=('build', 'run'))
    depends_on('libffi')

    def setup_build_environment(self, env):
        # This sets the compiler (and flags) that distutils will use
        # to create the final shared library.  It will use the
        # compiler specified by the environment variable 'CC' for all
        # other compilation.  We are setting 'LDSHARED' to the
        # spack compiler wrapper plus a few extra flags necessary for
        # building the shared library.
        if not sys.platform == 'darwin':
            env.set('LDSHARED', '{0} -shared -pthread'.format(spack_cc))
