# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestFlake8(PythonPackage):
    """pytest plugin to check FLAKE8 requirements."""

    homepage = "https://github.com/tholo/pytest-flake8"
    url      = "https://pypi.io/packages/source/p/pytest-flake8/pytest-flake8-0.8.1.tar.gz"

    version('0.8.1', sha256='aa10a6db147485d71dad391d4149388904c3072194d51755f64784ff128845fd')

    depends_on('py-setuptools', type='build')

    # Install requires:
    depends_on('py-flake8@3.0:', type=('build', 'run'))
    depends_on('py-pytest@2.8:', type=('build', 'run'))
