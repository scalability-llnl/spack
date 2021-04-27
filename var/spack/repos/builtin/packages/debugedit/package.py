# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Debugedit(AutotoolsPackage):
    """
    Debugedit was originally part of the rpm project, and is currently
    being refactored to be provided outside of it. This source will
    eventually be moved to sourceware or similar, as it is being maintained
    by RedHat.
    """

    homepage = "https://code.wildebeest.org/git/user/mjw/debugedit"
    git      = "git://code.wildebeest.org/user/mjw/debugedit"

    version('develop', branch='main')

    depends_on('pkgconfig', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('elfutils')  # requires libdw
    depends_on('libiberty')

    def build(self, spec, prefix):
        # requires libiberty
        libiberty = spec['libiberty'].prefix.include.libiberty
        make('CPPFLAGS=-I%s' % libiberty)
