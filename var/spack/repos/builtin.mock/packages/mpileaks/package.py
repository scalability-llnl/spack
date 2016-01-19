##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

class Mpileaks(Package):
    homepage = "http://www.llnl.gov"
    url      = "http://www.llnl.gov/mpileaks-1.0.tar.gz"

    version(1.0, 'foobarbaz')
    version(2.1, 'foobarbaz')
    version(2.2, 'foobarbaz')
    version(2.3, 'foobarbaz')

    variant('debug', default=False, description='Debug variant')
    variant('opt',   default=False, description='Optimized variant')

    depends_on("mpi")
    depends_on("callpath")

    def install(self, spec, prefix):
        pass
