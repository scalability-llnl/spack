# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRadicalUtils(PythonPackage):
    """RADICAL-Utils contains shared code and tools for various
    RADICAL-Cybertools packages."""

    homepage = 'https://radical-cybertools.github.io'
    git      = 'https://github.com/radical-cybertools/radical.utils.git'
    pypi     = 'radical.utils/radical.utils-1.6.7.tar.gz'

    maintainers = ['andre-merzky']

    version('devel', branch='devel')
    version('1.6.7', sha256='552f6c282f960ccd9d2401d686b0b3bfab35dfa94a26baeb2d3b4e45211f05a9')

    depends_on('py-radical-gtod',       type=('build', 'run'))
    depends_on('py-radical-gtod@devel', type=('build', 'run'), when='@devel')

    depends_on('python@3.6:',           type=('build', 'run'))
    depends_on('py-colorama',           type=('build', 'run'))
    depends_on('py-msgpack',            type=('build', 'run'))
    depends_on('py-netifaces',          type=('build', 'run'))
    depends_on('py-ntplib',             type=('build', 'run'))
    depends_on('py-pymongo',            type=('build', 'run'))
    depends_on('py-pyzmq',              type=('build', 'run'))
    depends_on('py-regex',              type=('build', 'run'))
    depends_on('py-setproctitle',       type=('build', 'run'))
    depends_on('py-setuptools',         type='build')
