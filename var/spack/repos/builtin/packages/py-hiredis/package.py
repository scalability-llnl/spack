# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHiredis(PythonPackage):
    """Python extension that wraps protocol parsing code in hiredis."""

    homepage = "https://github.com/redis/hiredis-py"
    url      = "https://files.pythonhosted.org/packages/3d/9f/abc69e73055f73d42ddf9c46b3e01a08b9e74b579b8fc413cbd31112a749/hiredis-1.1.0.tar.gz"

    version('1.1.0', sha256='996021ef33e0f50b97ff2d6b5f422a0fe5577de21a8873b58a779a5ddd1c3132')

    depends_on('python@2.7,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
