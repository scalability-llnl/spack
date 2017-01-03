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
from spack import *
from os import environ


class Zlib(AutotoolsPackage):
    """A free, general-purpose, legally unencumbered lossless
       data-compression library."""

    homepage = "http://zlib.net"
    url = "http://zlib.net/zlib-1.2.10.tar.gz"

    version('1.2.10', 'd9794246f853d15ce0fcbf79b9a3cf13')
    version('1.2.8', '44d667c142d7cda120332623eab69f40',
            url='http://pkgs.fedoraproject.org/repo/pkgs/mingw-zlib/zlib-1.2.8.tar.gz/44d667c142d7cda120332623eab69f40/zlib-1.2.8.tar.gz'
           )

    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    def configure(self, spec, prefix):

        if '+pic' in spec:
            environ['CFLAGS'] = self.compiler.pic_flag

        config_args = ['--prefix', prefix]
        configure(*config_args)
