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


class Zfp(MakefilePackage):
    """zfp is an open source C library for compressed floating-point arrays
       that supports very high throughput read and write random acces,
       target error bounds or bit rates.  Although bit-for-bit lossless
       compression is not always possible, zfp is usually accurate to
       within machine epsilon in near-lossless mode, and is often orders
       of magnitude more accurate than other lossy compressors. Versions
       of zfp 0.5.1 or newer also support compression of integer data.
    """

    homepage = "http://computation.llnl.gov/projects/floating-point-compression"
    url      = "http://computation.llnl.gov/projects/floating-point-compression/download/zfp-0.5.1.tar.gz"

    version('0.5.1', '0ed7059a9b480635e0dd33745e213d17')
    version('0.5.0', '2ab29a852e65ad85aae38925c5003654')

    variant('bswtuint8', default=False,
            description='Build with bit stream word type of uint8')

    def edit(self, spec, prefix):
        if '+bswtuint8' in self.spec:
            config_file = FileFilter('Config')
            config_file.filter(
                '^\s*#\s*DEFS\s*\+=\s*-DBIT_STREAM_WORD_TYPE\s*=\s*uint8',
                'DEFS += -DBIT_STREAM_WORD_TYPE=uint8')
 
    def build(self, spec, prefix):
        make("shared")

    def install(self, spec, prefix):
        incdir = 'include' if spec.satisfies('@0.5.1:') else 'inc'

        # No install provided
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        install('lib/libzfp.so', prefix.lib)
        install('%s/zfp.h' % incdir, prefix.include)
        install('%s/bitstream.h' % incdir, prefix.include)
        if spec.satisfies('@0.5.1:'):
            mkdirp('%s/zfp' % prefix.include)
            install('%s/zfp/system.h' % incdir, '%s/zfp' % prefix.include)
            install('%s/zfp/types.h' % incdir, '%s/zfp' % prefix.include)
        else:
            install('%s/types.h' % incdir, prefix.include)
            install('%s/system.h' % incdir, prefix.include)
