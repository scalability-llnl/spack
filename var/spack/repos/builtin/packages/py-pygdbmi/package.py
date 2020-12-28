# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygdbmi(PythonPackage):
    """Parse gdb machine interface output with Python"""

    homepage = "https://github.com/cs01/pygdbmi"
    url      = "https://pypi.io/packages/source/p/pygdbmi/pygdbmi-0.8.2.0.tar.gz"

    version('0.9.0.3', sha256='5bdf2f072e8f2f6471f19f8dcd87d6425c5d8069d47c0a5ffe8d0eff48cb171e')
    version('0.8.2.0', sha256='47cece65808ca42edf6966ac48e2aedca7ae1c675c4d2f0d001c7f3a7fa245fe')

    depends_on('python@3.5:', type=('build', 'run'), when='@0.9.0.3:')
    depends_on('python@2.7:2.8,3.4:3.6', type=('build', 'run'), when='@0.9.0.0:0.9.0.2')
    depends_on('python@2.7:2.8,3.3:3.6', type=('build', 'run'), when='@:0.8.4.0')
    depends_on('py-setuptools', type='build')
