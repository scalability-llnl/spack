# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCsvkit(PythonPackage):
    """A library of utilities for working with CSV, the king of tabular file
    formats"""

    homepage = 'http://csvkit.rtfd.org/'
    url      = "https://pypi.io/packages/source/c/csvkit/csvkit-0.9.1.tar.gz"

    version('1.0.4', sha256='1353a383531bee191820edfb88418c13dfe1cdfa9dd3dc46f431c05cd2a260a0')
    version('0.9.1', sha256='92f8b8647becb5cb1dccb3af92a13a4e85702d42ba465ce8447881fb38c9f93a')

    depends_on('py-setuptools',          type=('build', 'run'))
    depends_on('py-six@1.6.1:',          type=('build', 'run'))
    depends_on('py-argparse@1.2.1:',     type=('build', 'run'), when='^python@:2.6')
    depends_on('py-ordereddict@1.1:',    type=('build', 'run'), when='^python@:2.6')
    depends_on('py-simplejson@3.6.3:',   type=('build', 'run'), when='^python@:2.6')
    depends_on('py-python-dateutil@2.2', type=('build', 'run'), when='@0.9.1')
    depends_on('py-dbf@0.94.003',        type=('build', 'run'), when='@0.9.1')
    depends_on('py-xlrd@0.7.1:',         type=('build', 'run'), when='@0.9.1')
    depends_on('py-sqlalchemy@0.6.6:',   type=('build', 'run'), when='@0.9.1')
    depends_on('py-openpyxl@2.2.0-b1',   type=('build', 'run'), when='@0.9.1')
    depends_on('py-agate@1.6.1:',        type=('build', 'run'), when='@1:')
    depends_on('py-agate-excel@0.2.2:',  type=('build', 'run'), when='@1:')
    depends_on('py-agate-dbf@0.2.0:',    type=('build', 'run'), when='@1:')
    depends_on('py-agate-sql@0.5.3:',    type=('build', 'run'), when='@1:')
