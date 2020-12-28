# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyparsing(PythonPackage):
    """A Python Parsing Module."""
    homepage = "http://pyparsing.wikispaces.com/"
    url      = "https://pypi.io/packages/source/p/pyparsing/pyparsing-2.4.2.tar.gz"

    version('2.4.2',  sha256='6f98a7b9397e206d78cc01df10131398f1c8b8510a2f4d97d9abd82e1aacdd80')
    version('2.4.0',  sha256='1873c03321fc118f4e9746baf201ff990ceb915f433f23b395f5580d1840cb2a')
    version('2.3.1',  sha256='66c9268862641abcac4a96ba74506e594c884e3f57690a696d21ad8210ed667a')
    version('2.2.0',  sha256='0832bcf47acd283788593e7a0f542407bd9550a55a8a8435214a1960e04bcb04')
    version('2.1.10', sha256='811c3e7b0031021137fc83e051795025fcb98674d07eb8fe922ba4de53d39188')
    version('2.0.3',  sha256='06e729e1cbf5274703b1f47b6135ed8335999d547f9d8cf048b210fb8ebf844f')

    patch('setuptools-import.patch', when='@:2.1.10')

    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    # Newer versions of setuptools require pyparsing. Although setuptools is an
    # optional dependency of pyparsing, if it is not found, setup.py will
    # fallback on distutils.core instead. Don't add a setuptools dependency
    # or we won't be able to bootstrap setuptools.
    depends_on('py-setuptools', type='build', when='@2.3.1:')
