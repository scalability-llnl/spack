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


class Cfitsio(Package):
    """CFITSIO is a library of C and Fortran subroutines for reading and writing
    data files in FITS (Flexible Image Transport System) data format.
    """

    homepage = 'http://heasarc.gsfc.nasa.gov/fitsio/'

    version('3.370', 'abebd2d02ba5b0503c633581e3bfa116')

    def url_for_version(self, v):
        url = 'ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio{0}.tar.gz'
        return url.format(str(v).replace('.', ''))

    def install(self, spec, prefix):
        configure('--prefix=' + prefix)
        make()
        make('install')
