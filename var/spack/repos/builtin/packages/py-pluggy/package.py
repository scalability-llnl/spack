# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPluggy(PythonPackage):
    """Plugin and hook calling mechanisms for python."""

    homepage = "https://github.com/pytest-dev/pluggy"
    url      = "https://pypi.io/packages/source/p/pluggy/pluggy-0.13.0.tar.gz"

    version('0.13.0', sha256='fa5fa1622fa6dd5c030e9cad086fa19ef6a0cf6d7a2d12318e10cb49d6d68f34')
    version('0.12.0', sha256='0825a152ac059776623854c1543d65a4ad408eb3d33ee114dff91e57ec6ae6fc')
    version('0.7.1', sha256='95eb8364a4708392bae89035f45341871286a333f749c3141c20573d2b3876e1')
    version('0.6.0', sha256='7f8ae7f5bdf75671a718d2daf0a64b7885f74510bcd98b1a0bb420eb9a9d0cff')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-importlib-metadata@0.12:', when='^python@:3.7', type=('build', 'run'))
