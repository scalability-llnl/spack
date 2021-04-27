# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyPytestRunner(PythonPackage):
    """Invoke py.test as distutils command with dependency resolution."""

    homepage = "https://github.com/pytest-dev/pytest-runner"
    pypi = "pytest-runner/pytest-runner-5.1.tar.gz"

    version('5.1',    sha256='25a013c8d84f0ca60bb01bd11913a3bcab420f601f0f236de4423074af656e7a')
    version('2.11.1', sha256='983a31eab45e375240e250161a556163bc8d250edaba97960909338c273a89b3')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm@1.15:', type='build')
