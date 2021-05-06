# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonFedora(PythonPackage):
    """A Python library for interacting with, and connecting to,
    Fedora services."""

    homepage = "https://github.com/fedora-infra/python-fedora"
    pypi     = "python-fedora/python-fedora-1.1.1.tar.gz"

    version('1.1.1', sha256='56b9d841a39b4030e388e90c7b77dacd479f1ce5e2ff9b18c3954d97d5709a19')
    version('1.1.0', sha256='8cca046074001cedec0f7af5f80b288ff588c596fa1d4ff983251984e9b4fcaa')
    version('1.0.0', sha256='efb675929ebf588c2deffa2058ff407e65d1889bca1b545a58f525135367c9e4')

    depends_on('py-setuptools', type='build')
    depends_on('py-munch', type=('build', 'run'))
    depends_on('py-kitchen', type=('build', 'run'))
    depends_on('py-beautifulsoup4', type=('build', 'run'))
    depends_on('py-openidc-client', type=('build', 'run'))
    depends_on('py-urllib3', type=('build', 'run'))
    depends_on('py-six@1.4.0:', type=('build', 'run'))
    depends_on('py-lockfile', type=('build', 'run'))
