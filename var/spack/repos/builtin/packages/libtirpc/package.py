# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtirpc(AutotoolsPackage):
    """Libtirpc is a port of Suns Transport-Independent RPC library to Linux.
    """

    homepage = "https://sourceforge.net/projects/libtirpc/"
    url      = "https://sourceforge.net/projects/libtirpc/files/libtirpc/1.1.4/libtirpc-1.1.4.tar.bz2/download"

    version('1.2.6', sha256='4278e9a5181d5af9cd7885322fdecebc444f9a3da87c526e7d47f7a12a37d1cc')
    version('1.1.4', sha256='2ca529f02292e10c158562295a1ffd95d2ce8af97820e3534fe1b0e3aec7561d')

    depends_on('krb5')

    provides('rpc')

    # FIXME: build error on macOS
    # auth_none.c:81:9: error: unknown type name 'mutex_t'
    conflicts('platform=darwin', msg='Does not build on macOS')
