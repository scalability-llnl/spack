# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ManDb(AutotoolsPackage):
    """man-db is an implementation of the standard Unix
    documentation system accessed using the man command. It uses
    a Berkeley DB database in place of the traditional
    flat-text whatis databases."""

    homepage = "http://www.nongnu.org/man-db/"
    url      = "http://git.savannah.nongnu.org/cgit/man-db.git/snapshot/man-db-2.7.6.1.tar.gz"

    version('2.7.6.1', sha256='dd913662e341fc01e6721878b6cbe1001886cc3bfa6632b095937bba3238c779')

    depends_on('autoconf')
    depends_on('automake')
    depends_on('gettext')
    depends_on('libpipeline')
    depends_on('flex')
    depends_on('gdbm')
    depends_on('groff', type=('build', 'link', 'run'))

    # TODO: add gzip support via a new package.
    # man pages are typically compressed, include all available
    # compression libraries
    depends_on('bzip2', type=('build', 'link', 'run'))
    depends_on('xz',    type=('build', 'link', 'run'))

    def configure_args(self):
        args = [
            '--disable-setuid',
            # defaults to a location that needs root privs to write in
            '--with-systemdtmpfilesdir={0}/tmp'.format(self.prefix)
        ]
        return args
