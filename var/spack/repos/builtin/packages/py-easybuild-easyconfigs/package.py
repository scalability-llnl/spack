# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEasybuildEasyconfigs(PythonPackage):
    """Collection of easyconfig files for EasyBuild, a software build and
    installation framework for (scientific) software on HPC systems.
    """

    homepage = 'https://easybuilders.github.io/easybuild'
    url      = 'https://pypi.io/packages/source/e/easybuild-easyconfigs/easybuild-easyconfigs-4.0.0.tar.gz'
    maintainers = ['boegel']

    version('4.0.0', sha256='90d4e8f8abb11e7ae2265745bbd1241cd69d02570e9b4530175c4b2e2aba754e')
    version('3.1.2', sha256='621d514bacd9a0a9a3d35b40dcc448533ffc545b2c79f50d303822778bcc4aa5')

    depends_on('python@2.6:2.8', when='@:3', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.5:', when='@4:', type=('build', 'run'))

    for v in ['@3.1.2', '@4.0.0']:
        depends_on('py-easybuild-framework{0}:'.format(v), when=v + ':', type='run')
        depends_on('py-easybuild-easyblocks{0}:'.format(v), when=v, type='run')
