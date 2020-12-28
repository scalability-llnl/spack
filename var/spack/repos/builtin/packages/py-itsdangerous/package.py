# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyItsdangerous(PythonPackage):
    """Various helpers to pass trusted data to untrusted environments."""

    homepage = "http://github.com/mitsuhiko/itsdangerous"
    url = "https://pypi.io/packages/source/i/itsdangerous/itsdangerous-1.1.0.tar.gz"

    version('1.1.0', sha256='321b033d07f2a4136d3ec762eac9f16a10ccd60f53c0c91af90217ace7ba1f19')
    version('0.24',  sha256='cbb3fcf8d3e33df861709ecaf89d9e6629cff0a217bc2848f1b41cd30d360519')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
