# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyCheetah(PythonPackage):
    """Cheetah is a template engine and code generation tool."""

    pypi = "Cheetah/Cheetah-2.3.0.tar.gz"

    version('2.4.4', sha256='be308229f0c1e5e5af4f27d7ee06d90bb19e6af3059794e5fd536a6f29a9b550')
    version('2.3.0', sha256='2a32d7f7f70be98c2d57aa581f979bc799d4bf17d09fc0e7d77280501edf3e53')

    depends_on('python@2:2.99.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-markdown@2.0.1:', type=('build', 'run'))
