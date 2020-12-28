# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlye(PythonPackage):
    """Fast and accurate de novo assembler for single molecule sequencing
       reads"""

    homepage = "https://github.com/fenderglass/Flye"
    url      = "https://github.com/fenderglass/Flye/archive/2.6.tar.gz"

    version('2.6',   sha256='5bdc44b84712794fa4264eed690d8c65c0d72f495c7bbf2cd15b634254809131')
    version('2.4.2', sha256='5b74d4463b860c9e1614ef655ab6f6f3a5e84a7a4d33faf3b29c7696b542c51a')

    # https://github.com/fenderglass/Flye/blob/flye/docs/INSTALL.md
    depends_on('python@2.7:2.8,3.5:', when='@2.6:', type=('build', 'run'))
    depends_on('python@2.7:2.8',      when='@:2.5', type=('build', 'run'))
    depends_on('py-setuptools', when='@2.6:', type='build')
    depends_on('gmake', type='build')
    depends_on('zlib')

    msg = 'C++ compiler with C++11 support required'
    conflicts('%gcc@:4.7',   msg=msg)
    conflicts('%clang@:3.2', msg=msg)
    conflicts('%apple-clang@:4.9', msg=msg)

    def setup_build_environment(self, env):
        if self.spec.target.family == 'aarch64':
            env.set('arm_neon', '1')
            env.set('aarch64', '1')
