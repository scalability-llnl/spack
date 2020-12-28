# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestMypy(PythonPackage):
    """Mypy static type checker plugin for Pytest."""

    homepage = "https://github.com/dbader/pytest-mypy"
    url      = "https://pypi.io/packages/source/p/pytest-mypy/pytest-mypy-0.4.2.tar.gz"

    version('0.4.2', sha256='5a5338cecff17f005b181546a13e282761754b481225df37f33d37f86ac5b304')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest@2.8:',    when='^python@3.5:', type=('build', 'run'))
    depends_on('py-pytest@2.8:4.6', when='^python@:3.4', type=('build', 'run'))
    depends_on('py-mypy@0.500:0.699', when='^python@:3.4',    type=('build', 'run'))
    depends_on('py-mypy@0.500:',      when='^python@3.5:3.7', type=('build', 'run'))
    depends_on('py-mypy@0.700:',      when='^python@3.8:',    type=('build', 'run'))
