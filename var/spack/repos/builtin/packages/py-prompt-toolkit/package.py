# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPromptToolkit(PythonPackage):
    """Library for building powerful interactive command lines in Python"""

    homepage = "https://pypi.python.org/pypi/prompt_toolkit"
    url      = "https://pypi.io/packages/source/p/prompt_toolkit/prompt_toolkit-1.0.9.tar.gz"

    version('3.0.7',  sha256='822f4605f28f7d2ba6b0b09a31e25e140871e96364d1d377667b547bb3bf4489')
    version('2.0.9',  sha256='2519ad1d8038fd5fc8e770362237ad0364d16a7650fb5724af6997ed5515e3c1')
    version('1.0.16', sha256='c1cedd626e08b8ee830ee65897de754113ff3f3035880030c08b01674d85c5b4')
    version('1.0.9',  sha256='cd6523b36adc174cc10d54b1193eb626b4268609ff6ea92c15bcf1996609599c')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.9.0:', type=('build', 'run'))
    depends_on('py-wcwidth', type=('build', 'run'))
