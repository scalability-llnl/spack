# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Easybuild(PythonPackage):
    """EasyBuild is a software build and installation framework
    for (scientific) software on HPC systems.
    """

    homepage = 'https://easybuilders.github.io/easybuild/'
    url      = 'https://pypi.io/packages/source/e/easybuild/easybuild-4.0.0.tar.gz'
    maintainers = ['boegel']

    version('4.0.0', sha256='21bcc1048525ad6219667cc97a7421b5388068c670cabba356712e474896de40')
    version('3.1.2', sha256='a966a08e41d3557d7fd3dc5322180c006d27281d9ecc1b1fce1b4518c32664d4')

    depends_on('python@2.6:2.8', when='@:3', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.5:', when='@4:', type=('build', 'run'))

    for v in ['@4.0.0', '@3.1.2']:
        depends_on('py-easybuild-framework'   + v, when=v, type='run')
        depends_on('py-easybuild-easyblocks'  + v, when=v, type='run')
        depends_on('py-easybuild-easyconfigs' + v, when=v, type='run')
