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

class Caliper(Package):
    """
    Caliper is a generic context annotation system. It gives programmers the
    ability to provide arbitrary program context information to (performance)
    tools at runtime.
    """

    homepage = "https://github.com/LLNL/Caliper"
    url      = ""

    version('master', git='https://github.com/LLNL/Caliper.git')

    variant('mpi', default=False, description='Enable MPI function wrappers.')

    depends_on('libunwind')
    depends_on('papi')
    depends_on('mpi', when='+mpi')
    depends_on('cmake', type='build')

    def install(self, spec, prefix):
      with working_dir('build', create=True):
        cmake('..', *std_cmake_args)
        make()
        make("install")
