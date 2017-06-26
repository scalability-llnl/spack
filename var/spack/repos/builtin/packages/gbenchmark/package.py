##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
from spack import *


class Gbenchmark(CMakePackage):
    """A microbenchmark support library"""

    homepage = "https://github.com/google/benchmark"
    url = "https://github.com/google/benchmark/archive/v1.0.0.tar.gz"

    version('1.1.0', '8c539bbe2a212618fa87b6c38fba087100b6e4ae')
    version('1.0.0', '4f778985dce02d2e63262e6f388a24b595254a93')

    def build_type(self):
        return "Release"

    def patch(self):
        filter_file(
            r'add_cxx_compiler_flag..fstrict.aliasing.',
            r'##### add_cxx_compiler_flag(-fstrict-aliasing)',
            'CMakeLists.txt'
        )
        filter_file(
            r'add_cxx_compiler_flag..Werror',
            r'##### add_cxx_compiler_flag(-Werror',
            'CMakeLists.txt'
        )
