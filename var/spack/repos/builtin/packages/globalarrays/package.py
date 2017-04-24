##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at IBM.
#
# This file is part of Spack.
# Created by Serban Maerean, serban@ibm.com, All rights reserved.
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install globalarrays
#
# You can edit this file again by typing:
#
#     spack edit globalarrays
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Globalarrays(CMakePackage):
    """The Global Arrays (GA) toolkit provides a shared memory style programming
    environment in the context of distributed array data structures.
    """

    homepage = "http://hpc.pnl.gov/globalarrays/"
    url      = "https://github.com/GlobalArrays/ga"

    version('master', git='https://github.com/GlobalArrays/ga', branch='master')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi')

    patch('ibm-xl.patch', when='%xl')
    patch('ibm-xl.patch', when='%xl_r')

    def cmake_args(self):
        options = []

        options.extend([
            '-DENABLE_FORTRAN=ON',
            '-DENABLE_BLAS=ON',
        ])

        if self.compiler.name == 'xl' or self.compiler.name == 'xl_r':
            # use F77 compiler if IBM XL
            options.extend([
                '-DCMAKE_Fortran_COMPILER=%s' % self.compiler.f77,
                '-DCMAKE_Fortran_FLAGS=-qzerosize'
            ])
        
        return options
