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


class Cgns(Package):
    """The CFD General Notation System (CGNS) provides a general, portable,
    and extensible standard for the storage and retrieval of computational
    fluid dynamics (CFD) analysis data."""

    homepage = "http://cgns.github.io/"
    url      = "https://github.com/CGNS/CGNS/archive/v3.3.0.tar.gz"

    version('3.3.0', '64e5e8d97144c1462bee9ea6b2a81d7f')

    variant('hdf5', default=True, description='Enable HDF5 interface')

    depends_on('cmake', type='build')
    depends_on('hdf5', when='+hdf5')

    def install(self, spec, prefix):
        cmake_args = std_cmake_args[:]

        if self.compiler.f77 and self.compiler.fc:
            cmake_args.append('-DCGNS_ENABLE_FORTRAN=ON')
        else:
            cmake_args.append('-DCGNS_ENABLE_FORTRAN=OFF')

        if '+hdf5' in spec:
            cmake_args.extend([
                '-DCGNS_ENABLE_HDF5=ON',
                '-DHDF5_NEEDS_ZLIB=ON'
            ])

            if spec.satisfies('^hdf5+mpi'):
                cmake_args.append('-DHDF5_NEEDS_MPI=ON')
            else:
                cmake_args.append('-DHDF5_NEEDS_MPI=OFF')

            if spec.satisfies('^hdf5+szip'):
                cmake_args.append('-DHDF5_NEEDS_SZIP=ON')
            else:
                cmake_args.append('-DHDF5_NEEDS_SZIP=OFF')
        else:
            cmake_args.append('-DCGNS_ENABLE_HDF5=OFF')

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)

            make()
            make('install')
