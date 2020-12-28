# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAutopep8(PythonPackage):
    """autopep8 automatically formats Python code to conform to the
    PEP 8 style guide."""

    homepage = "https://github.com/hhatto/autopep8"
    url      = "https://pypi.io/packages/source/a/autopep8/autopep8-1.2.4.tar.gz"

    version('1.4.4', sha256='4d8eec30cc81bc5617dbf1218201d770dc35629363547f17577c61683ccfb3ee')
    version('1.3.3', sha256='ff787bffb812818c3071784b5ce9a35f8c481a0de7ea0ce4f8b68b8788a12f30')
    version('1.2.4', sha256='38e31e266e29808e8a65a307778ed8e402e1f0d87472009420d6d18146cdeaa2')
    version('1.2.2', sha256='ecc51614755c7f697e83478f87eb6bbd009075a397c15080f0311aaecbbdfca8')

    extends('python', ignore='bin/pep8')
    depends_on('python@2.6:2.8,3.2:', type=('build', 'run'))

    depends_on('py-pycodestyle@1.5.7:1.7.0', type=('build', 'run'), when='@:1.2.4')
    depends_on('py-pycodestyle@2.3.0:', type=('build', 'run'), when='@1.3:')
    depends_on('py-pycodestyle@2.4.0:', type=('build', 'run'), when='@1.4:')

    depends_on('py-setuptools', type='build')
