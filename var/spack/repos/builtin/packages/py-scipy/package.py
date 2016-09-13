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


class PyScipy(Package):
    """Scientific Library for Python."""
    homepage = "http://www.scipy.org/"
    url      = "https://pypi.python.org/packages/source/s/scipy/scipy-0.15.0.tar.gz"

    version('0.17.0', '5ff2971e1ce90e762c59d2cd84837224')
    version('0.15.1', 'be56cd8e60591d6332aac792a5880110')
    version('0.15.0', '639112f077f0aeb6d80718dc5019dc7a')

    extends('python')
    depends_on('py-nose', type='build')
#    depends_on('binutils@2.26:', type='build')
    depends_on('py-numpy+blas+lapack', type=nolink)


    def install(self, spec, prefix):
        if 'atlas' in spec:
            # libatlas.so actually isn't always installed, but this
            # seems to make the build autodetect things correctly.
            env['ATLAS'] = join_path(
                spec['atlas'].prefix.lib, 'libatlas.' + dso_suffix)
        else:
            blas_spec = spec['blas']
            try:
                env['BLAS']   = blas_spec.blas_shared_lib
            except AttributeError:
                # This installation has not shared lib; use static
                env['BLAS']   = blas_spec.blas_static_lib

            lapack_spec = spec['lapack']
            try:
                env['LAPACK']   = lapack_spec.lapack_shared_lib
            except AttributeError:
                # This installation has not shared lib; use static
                env['LAPACK']   = lapack_spec.lapack_static_lib

        python('setup.py', 'install', '--prefix=%s' % prefix)
