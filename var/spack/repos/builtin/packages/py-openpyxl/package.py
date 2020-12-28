# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenpyxl(PythonPackage):
    """A Python library to read/write Excel 2010 xlsx/xlsm files"""

    homepage = "http://openpyxl.readthedocs.org/"
    url      = "https://pypi.io/packages/source/o/openpyxl/openpyxl-3.0.3.tar.gz"

    version('3.0.3', sha256='547a9fc6aafcf44abe358b89ed4438d077e9d92e4f182c87e2dc294186dc4b64')
    version('2.4.5', sha256='78c331e819fb0a63a1339d452ba0b575d1a31f09fdcce793a31bec7e9ef4ef21')

    depends_on('python@3.6:',         when='@3.0:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@2.6:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@2.5:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', when='@2.1:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')

    depends_on('py-jdcal',      type=('build', 'run'))
    depends_on('py-et-xmlfile', type=('build', 'run'))
