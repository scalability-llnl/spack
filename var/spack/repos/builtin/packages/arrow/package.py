##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Arrow(CMakePackage):
    """A cross-language development platform for in-memory data.

    This package contains the C++ bindings.
    """

    homepage = "http://arrow.apache.org"
    url      = "https://github.com/apache/arrow/archive/apache-arrow-0.9.0.tar.gz"

    version('0.9.0', 'ebbd36c362b9e1d398ca612f6d2531ec')
    version('0.8.0', '56436f6f61ccc68686b7e0ea30bf4d09')

    depends_on('boost@1.60:')
    depends_on('cmake@3.2.0:')
    depends_on('flatbuffers@1.8.0')
    depends_on('rapidjson')
    depends_on('snappy')
    depends_on('zlib')
    depends_on('zstd')

    variant('build_type', default='Release')
    # variant('shared', default=False)

    def cmake(self, spec, prefix):
        args = std_cmake_args + [
            "-DARROW_USE_SSE=ON",
            "-DARROW_BUILD_SHARED=ON",
            "-DARROW_BUILD_STATIC=OFF",
            "-DARROW_BUILD_TESTS=OFF",
            "-DARROW_WITH_BROTLI=OFF",
            "-DARROW_WITH_LZ4=OFF",
        ]
        for dep in ('flatbuffers', 'rapidjson', 'snappy', 'zlib', 'zstd'):
            args.append("-D{}_HOME={}".format(dep.upper(), spec[dep].prefix))
        args.append("-DZLIB_LIBRARIES={}".format(spec['zlib'].libs))
        with working_dir(self.build_directory, create=True):
            cmake(join_path(self.stage.source_path, 'cpp'), *args)

    @run_after('cmake')
    def patch_flags(self):
        for root, dirs, files in os.walk(self.build_directory):
            if 'flags.make' not in files:
                continue
            fn = os.path.join(root, 'flags.make')
            with open(fn) as fd:
                data = fd.read()
            with open(fn, 'w') as fd:
                fd.write(data.replace('-isystem /usr/include', ''))
