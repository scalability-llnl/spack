# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyKeyring(PythonPackage):
    """The Python keyring library provides an easy way to access the system keyring
    service from python. It can be used in any application that needs safe password
    storage."""

    homepage = "https://github.com/jaraco/keyring"
    pypi     = "keyring/keyring-23.0.1.tar.gz"

    version('23.0.1', sha256='045703609dd3fccfcdb27da201684278823b72af515aedec1a8515719a038cb8')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@3.4.1:+toml', type='build')
    depends_on('py-importlib-metadata@3.6:', type=('build', 'run'))
    # TODO: additional dependencies required for Windows/Linux
