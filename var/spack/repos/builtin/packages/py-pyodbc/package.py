# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyodbc(PythonPackage):
    """A Python DB API 2 module for ODBC. This project provides an up-to-date,
       convenient interface to ODBC using native data types like datetime and
       decimal."""

    homepage = "https://github.com/mkleehammer/pyodbc"
    url      = "https://pypi.io/packages/source/p/pyodbc/pyodbc-4.0.26.tar.gz"

    version('4.0.26', sha256='e52700b5d24a846483b5ab80acd9153f8e593999c9184ffea11596288fb33de3')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('unixodbc',        type=('build', 'run'))

    phases = ['build_ext', 'install']

    def build_ext_args(self, spec, prefix):

        args = (['--rpath=%s' % (spec['unixodbc'].prefix.lib)])
        return args
