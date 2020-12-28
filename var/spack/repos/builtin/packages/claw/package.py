# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Claw(CMakePackage):
    """CLAW Compiler targets performance portability problem in climate and
       weather application written in Fortran. From a single source code, it
       generates architecture specific code decorated with OpenMP or OpenACC"""

    homepage = 'https://claw-project.github.io/'
    git      = 'https://github.com/claw-project/claw-compiler.git'
    maintainers = ['clementval']

    version('master', branch='master', submodules=True)
    version('2.0.2', commit='8c012d58484d8caf79a4fe45597dc74b4367421c', submodules=True)
    version('2.0.1', commit='f5acc929df74ce66a328aa4eda9cc9664f699b91', submodules=True)
    version('2.0',   commit='53e705b8bfce40a5c5636e8194a7622e337cf4f5', submodules=True)
    version('1.2.3', commit='eaf5e5fb39150090e51bec1763170ce5c5355198', submodules=True)
    version('1.2.2', commit='fc27a267eef9f412dd6353dc0b358a05b3fb3e16', submodules=True)
    version('1.2.1', commit='939989ab52edb5c292476e729608725654d0a59a', submodules=True)
    version('1.2.0', commit='fc9c50fe02be97b910ff9c7015064f89be88a3a2', submodules=True)
    version('1.1.0', commit='16b165a443b11b025a77cad830b1280b8c9bcf01', submodules=True)

    depends_on('cmake@3.0:', type='build')
    depends_on('ant@1.9:', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')

    depends_on('java@8:', when="@2.0:")
    depends_on('java@7:', when="@1.1.0:1.2.3")
    depends_on('libxml2')

    patch('https://github.com/claw-project/claw-compiler/commit/e9fe6dbd291454ce34dd58f21d102f7f1bdff874.patch',
          sha256='44a3e17bf6e972db9760fc50bc0948309ee441dab1cdb11816ba675de0138549',
          when='@:2.0.2%intel')

    # Cache ANT dependencies in the stage directory.
    # Otherwise, they are cached to the user's home directory.
    patch('ivy_local_cache.patch')

    # https://github.com/claw-project/claw-compiler/pull/586
    conflicts('%nag', when='@:2.0.1')

    filter_compiler_wrappers('claw_f.conf', relative_root='etc')

    def cmake_args(self):
        args = [
            '-DOMNI_CONF_OPTION=--with-libxml2=%s' %
            self.spec['libxml2'].prefix
        ]

        return args
