# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAbslPy(PythonPackage):
    """
    This repository is a collection of Python library code for building
    Python applications.

    The code is collected from Google's own Python code base, and has been
    extensively tested and used in production.
    """

    homepage = "https://pypi.org/project/absl-py/"
    url      = "https://pypi.io/packages/source/a/absl-py/absl-py-0.7.0.tar.gz"

    version('0.7.1', sha256='b943d1c567743ed0455878fcd60bc28ac9fae38d129d1ccfad58079da00b8951')
    version('0.7.0', sha256='8718189e4bd6013bf79910b9d1cb0a76aecad8ce664f78e1144980fabdd2cd23')
    version('0.1.6', sha256='02c577d618a8bc0a2a5d1a51f160d3649745d7a2516d87025322f46ac1391a22')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3.99')
