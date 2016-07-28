##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
from spack import *

class Lmdb(Package):
    """Read-only mirror of official repo on openldap.org. Issues and
    pull requests here are ignored. Use OpenLDAP ITS for issues.
    http://www.openldap.org/software/repo.html"""


    homepage = "http://www.openldap.org/software/repo.html"
    url      = "https://github.com/LMDB/lmdb/archive/LMDB_0.9.16.tar.gz"

    version('0.9.16', '0de89730b8f3f5711c2b3a4ba517b648')

    def install(self, spec, prefix):
        os.chdir('libraries/liblmdb')

        make()

        mkdirp(prefix.bin)
        mkdirp(prefix + '/man/man1')
        mkdirp(prefix.lib)
        mkdirp(prefix.include)

        bins = ['mdb_stat', 'mdb_copy', 'mdb_dump', 'mdb_load']
        for f in bins:
            install(f, prefix.bin)

        mans = ['mdb_stat.1', 'mdb_copy.1', 'mdb_dump.1', 'mdb_load.1']
        for f in mans:
            install(f, prefix + '/man/man1')

        libs = ['liblmdb.a', 'liblmdb.so']
        for f in libs:
            install(f, prefix.lib)

        includes = ['lmdb.h']
        for f in includes:
            install(f, prefix.include)
