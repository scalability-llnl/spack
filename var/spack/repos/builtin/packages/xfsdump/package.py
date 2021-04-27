# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xfsdump(MakefilePackage):
    """XFS Dump Tools."""

    homepage = "http://oss.sgi.com/projects/xfs/"
    url      = "https://github.com/pcacjr/xfsdump/archive/v3.1.6.tar.gz"

    version('3.1.6', sha256='bbf659758107cad9b41cf3001df121e6428485b341109a1f1a952fd477a7010b')
    version('3.1.5', sha256='ba5bb91413ccb5a0eaffaa84f242baa08520a09f7b990b28bbd0d33a4390f7b6')
    version('3.1.4', sha256='a75d5c7dabd3dd4184008efcfd30d0c96b6ab318edaad9659ce180dfb9652b01')

    depends_on('gettext')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('util-linux')
    depends_on('attr')
    depends_on('xfsprogs@:4.20.0')

    def setup_build_environment(self, env):
        env.append_flags('LDFLAGS', '-lintl')

    def build(self, spec, prefix):
        make('prefix={0}'.format(self.prefix),
             'MSGFMT={0}'.format(self.spec['gettext'].prefix.bin.msgfmt),
             'MSGMERGE={0}'.format(self.spec['gettext'].prefix.bin.msgmerge),
             'XGETTEXT={0}'.format(self.spec['gettext'].prefix.bin.xgettext))

    def install(self, spec, prefix):
        make('prefix={0}'.format(self.prefix),
             'MSGFMT={0}'.format(self.spec['gettext'].prefix.bin.msgfmt),
             'MSGMERGE={0}'.format(self.spec['gettext'].prefix.bin.msgmerge),
             'XGETTEXT={0}'.format(self.spec['gettext'].prefix.bin.xgettext),
             'install')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix.sbin)
