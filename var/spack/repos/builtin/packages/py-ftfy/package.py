# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyFtfy(PythonPackage):
    """Fixes Unicode that's broken in various ways."""

    homepage = "https://ftfy.readthedocs.io"
    pypi     = "ftfy/ftfy-5.8.tar.gz"

    version('5.8', sha256='51c7767f8c4b47d291fcef30b9625fb5341c06a31e6a3b627039c706c42f3720')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-wcwidth', type=('build', 'run'))
