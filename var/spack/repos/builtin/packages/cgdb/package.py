# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cgdb(AutotoolsPackage):
    """A curses front-end to GDB"""

    homepage = "https://cgdb.github.io"
    url      = "https://cgdb.me/files/cgdb-0.7.0.tar.gz"

    version('0.7.0', sha256='bf7a9264668db3f9342591b08b2cc3bbb08e235ba2372877b4650b70c6fb5423')

    # Required dependency
    depends_on('ncurses')
    depends_on('readline')

    def configure_args(self):
        spec = self.spec

        return [
            '--with-ncurses={0}'.format(spec['ncurses'].prefix),
            '--with-readline={0}'.format(spec['readline'].prefix)
        ]
