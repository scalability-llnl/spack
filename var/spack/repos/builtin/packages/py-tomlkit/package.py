# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTomlkit(PythonPackage):
    """Style preserving TOML library"""

    homepage = "https://github.com/sdispater/tomlkit"
    url      = "https://pypi.io/packages/source/t/tomlkit/tomlkit-0.7.0.tar.gz"

    version('0.7.0', sha256='ac57f29693fab3e309ea789252fcce3061e19110085aa31af5446ca749325618')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-enum34@1.1:1.999', when='^python@:2', type=('build', 'run'))
    depends_on('py-functools32@3.2.3:3.999', when='^python@:2', type=('build', 'run'))
    depends_on('py-typing@3.6:3.999', when='^python@:3.4', type=('build', 'run'))
