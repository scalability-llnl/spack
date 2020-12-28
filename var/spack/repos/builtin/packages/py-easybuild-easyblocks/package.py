# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEasybuildEasyblocks(PythonPackage):
    """Collection of easyblocks for EasyBuild, a software build and
    installation framework for (scientific) software on HPC systems.
    """

    homepage = 'https://easybuilders.github.io/easybuild'
    url      = 'https://pypi.io/packages/source/e/easybuild-easyblocks/easybuild-easyblocks-4.0.0.tar.gz'
    maintainers = ['boegel']

    version('4.0.0', sha256='a0fdef6c33c786e323bde1b28bab942fd8e535c26842877d705e692e85b31b07')
    version('3.1.2', sha256='5dcea0d612c5da92815f2c99a591dd2843fe9d76f4c0f4ff4a245d43c39001d8')

    depends_on('python@2.6:2.8', when='@:3', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.5:', when='@4:', type=('build', 'run'))

    for v in ['@3.1.2', '@4.0.0']:
        depends_on('py-easybuild-framework' + v, when=v, type='run')
