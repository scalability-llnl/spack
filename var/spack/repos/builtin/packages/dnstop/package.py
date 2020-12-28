# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dnstop(AutotoolsPackage):
    """Stay on top of your DNS traffic."""

    homepage = "https://github.com/measurement-factory/dnstop"
    git      = "https://github.com/measurement-factory/dnstop.git"

    version('master', branch='master')

    depends_on('libpcap')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.share.man.man8)
        make('BINPATH={0}'.format(prefix.bin),
             'MANPATH={0}/'.format(prefix),
             'install')
