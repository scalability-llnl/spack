# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPromptToolkit(PythonPackage):
    """Library for building powerful interactive command lines in Python"""

    pypi = "prompt_toolkit/prompt_toolkit-1.0.9.tar.gz"

    version('3.0.17', sha256='9397a7162cf45449147ad6042fa37983a081b8a73363a5253dd4072666333137')
    version('3.0.16', sha256='0fa02fa80363844a4ab4b8d6891f62dd0645ba672723130423ca4037b80c1974')
    version('3.0.7',  sha256='822f4605f28f7d2ba6b0b09a31e25e140871e96364d1d377667b547bb3bf4489')
    version('2.0.10', sha256='f15af68f66e664eaa559d4ac8a928111eebd5feda0c11738b5998045224829db')
    version('2.0.9',  sha256='2519ad1d8038fd5fc8e770362237ad0364d16a7650fb5724af6997ed5515e3c1')
    version('1.0.16', sha256='c1cedd626e08b8ee830ee65897de754113ff3f3035880030c08b01674d85c5b4')
    version('1.0.9',  sha256='cd6523b36adc174cc10d54b1193eb626b4268609ff6ea92c15bcf1996609599c')

    depends_on('python@3.6.1:', when='@3:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', when='@:2.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.9.0:', when='@:2.999', type=('build', 'run'))
    depends_on('py-wcwidth', type=('build', 'run'))
