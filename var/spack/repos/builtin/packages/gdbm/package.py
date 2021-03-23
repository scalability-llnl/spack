# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Gdbm(AutotoolsPackage, GNUMirrorPackage):
    """GNU dbm (or GDBM, for short) is a library of database functions
    that use extensible hashing and work similar to the standard UNIX dbm.
    These routines are provided to a programmer needing to create and
    manipulate a hashed database."""

    homepage = "http://www.gnu.org.ua/software/gdbm/gdbm.html"
    gnu_mirror_path = "gdbm/gdbm-1.13.tar.gz"

    version('1.19',   sha256='37ed12214122b972e18a0d94995039e57748191939ef74115b1d41d8811364bc')
    version('1.18.1', sha256='86e613527e5dba544e73208f42b78b7c022d4fa5a6d5498bf18c8d6f745b91dc')
    version('1.14.1', sha256='cdceff00ffe014495bed3aed71c7910aa88bf29379f795abc0f46d4ee5f8bc5f')
    version('1.13',   sha256='9d252cbd7d793f7b12bcceaddda98d257c14f4d1890d851c386c37207000a253')
    version('1.12',   sha256='d97b2166ee867fd6ca5c022efee80702d6f30dd66af0e03ed092285c3af9bcea')
    version('1.11',   sha256='8d912f44f05d0b15a4a5d96a76f852e905d051bb88022fcdfd98b43be093e3c3')
    version('1.10',   sha256='23f8134c5b94bbfb06d756a6b78f074fba6e6028cf2fe01341d40b26db773441')
    version('1.9.1',  sha256='6025852637772b0699f2294b5f14fd4a084bca3c8161d29d64d1f30d6d1a9aed')
    version('1.9',    sha256='f85324d7de3777db167581fd5d3493d2daa3e85e195a8ae9afc05b34551b6e57')

    depends_on("readline")
    patch('gdbm.patch', when='@:1.18 %gcc@10:')
    patch('gdbm.patch', when='@:1.18 %clang@11:')
    patch('gdbm.patch', when='@:1.18 %cce@11:')
    patch('gdbm.patch', when='@:1.18 %aocc@2:')
    patch('gdbm.patch', when='@:1.18 %oneapi')

    def configure_args(self):

        # GDBM uses some non-standard GNU extensions,
        # enabled with -D_GNU_SOURCE.  See:
        #   https://patchwork.ozlabs.org/patch/771300/
        #   https://stackoverflow.com/questions/5582211
        #   https://www.gnu.org/software/automake/manual/html_node/Flag-Variables-Ordering.html
        return [
            '--enable-libgdbm-compat',
            'CPPFLAGS=-D_GNU_SOURCE']
