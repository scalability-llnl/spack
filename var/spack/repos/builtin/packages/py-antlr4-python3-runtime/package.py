# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAntlr4Python3Runtime(PythonPackage):
    """This package provides runtime libraries required to use
    parsers generated for the Python3 language by version 4 of
    ANTLR (ANother Tool for Language Recognition).
    """

    homepage = "https://www.antlr.org"
    url      = "https://pypi.io/packages/source/a/antlr4-python3-runtime/antlr4-python3-runtime-4.7.2.tar.gz"

    version('4.7.2', sha256='168cdcec8fb9152e84a87ca6fd261b3d54c8f6358f42ab3b813b14a7193bb50b')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
