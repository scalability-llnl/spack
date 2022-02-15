# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyassimp(PythonPackage):
    """Python bindings for the Open Asset Import Library (ASSIMP)"""

    homepage = "https://github.com/mikedh/pyassimp"
    pypi     = "pyassimp/pyassimp-4.1.4.tar.gz"

    version('4.1.4', sha256='266bd4be170d46065b8c2ad0f5396dad10938a6bbf9a566c4e4d56456e33aa6a')

    depends_on('py-numpy', type=('build', 'run'))
