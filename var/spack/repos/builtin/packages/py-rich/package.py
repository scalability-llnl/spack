# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRich(PythonPackage):
    """Rich is a Python library for rich text and beautiful formatting
    in the terminal.
    """

    homepage = "https://github.com/willmcgugan/rich"
    pypi     = "rich/rich-9.4.0.tar.gz"

    version('9.9.0', sha256='0bd8f42c3a03b7ef5e311d5e37f47bea9d268f541981c169072be5869c007957')
    version('9.8.2', sha256='c0d5903b463f015b254d6f52da82af3821d266fe516ae05fdc266e6abba5c3a8')
    version('9.8.1', sha256='0ec853f882613e75a5e46d545ddaa48cad235c616eaeb094792012fe22e8b2c6')
    version('9.8.0', sha256='c91c2587dba9aa8dd30c5f090e700f54433ccd73e209f4737e10385c4c1cbf19')
    version('9.7.0', sha256='25583ce533afae71de086ca97cf0aa883a5e1a220dfcc6049a2809a74bc79ca0')
    version('9.6.2', sha256='b6a7f9ef1a35c248498952d3454fb4f88de415dd989f97c3e5c5e2235d66e3a5')
    version('9.6.1', sha256='5ac9f4f7f6b0e32e7e412de127f15b94144e22c9a7896551474d640143bbaa7b')
    version('9.6.0', sha256='ae7f5f24fc90c76ccb54883f4bd633cbd146e0bbe3e070275ca97038ce53cf2f')
    version('9.5.1', sha256='8b937e2d2c4ff9dcfda8a5910a8cd384bd30f50ec92346d616f62065c662df5f')
    version('9.5.0', sha256='a65a9d003cb6e87e6fa5d1b53bff6f43a8d7475524c58873acdbf5bba0683fa3')
    version('9.4.0', sha256='bde23a1761373fed2802502ff98292c5d735a5389ed96f4fe1be5fb4c2cde8ea')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-typing-extensions@3.7.4:3.99', type=('build', 'run'))
    depends_on('py-dataclasses@0.7:0.8', when='^python@:3.6', type=('build', 'run'))
    depends_on('py-pygments@2.6:2.99', type=('build', 'run'))
    depends_on('py-commonmark@0.9.0:0.9.999', type=('build', 'run'))
    depends_on('py-colorama@0.4.0:0.4.999', type=('build', 'run'))
