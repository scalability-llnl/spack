# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPreCommit(PythonPackage):
    """A framework for managing and maintaining multi-language pre-commit
    hooks."""

    homepage = "https://github.com/pre-commit/pre-commit"
    url      = "https://pypi.io/packages/source/p/pre_commit/pre_commit-1.20.0.tar.gz"

    version('1.20.0', sha256='9f152687127ec90642a2cc3e4d9e1e6240c4eb153615cb02aa1ad41d331cbb6e')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-aspy-yaml', type=('build', 'run'))
    depends_on('py-cfgv@2.0.0:', type=('build', 'run'))
    depends_on('py-identify@1.0.0:', type=('build', 'run'))
    depends_on('py-nodeenv@0.11.1:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-toml', type=('build', 'run'))
    depends_on('py-virtualenv@15.2:', type=('build', 'run'))
    depends_on('py-futures', type=('build', 'run'), when='^python@:3.1.99')
    depends_on('py-importlib-metadata', type=('build', 'run'), when='^python@:3.7.99')
    depends_on('py-importlib-resources', type=('build', 'run'), when='^python@:3.6.99')
