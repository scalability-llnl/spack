##############################################################################
# Copyright (c) 2013-2022, Triad National Security, LLC.
# Produced at the Los Alamos National Laboratory.
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
from llnl.util.filesystem import LibraryList
from spack import *


class CrayLibsci(Package):
    """The Cray Scientific Libraries package, LibSci, is a collection of
    numerical routines optimized for best performance on Cray systems."""

    homepage = "http://www.nersc.gov/users/software/programming-libraries/math-libraries/libsci/"
    url      = "http://www.nersc.gov/users/software/programming-libraries/math-libraries/libsci/"

    version("18.11.1.2")
    version("16.11.1")
    version("16.09.1")
    version('16.07.1')
    version("16.06.1")
    version("16.03.1")

    provides("blas")
    provides("lapack")
    provides("scalapack")

    # NOTE: Cray compiler wrappers already include linking for the following
    @property
    def blas_libs(self):
        return LibraryList([self.prefix.lib])

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        return self.blas_libs

    def install(self, spec, prefix):
        raise NoBuildError(spec)
