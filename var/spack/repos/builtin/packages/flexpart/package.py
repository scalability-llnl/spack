# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Flexpart(MakefilePackage):
    """FLEXPART (FLEXible PARTicle dispersion model) is a Lagrangian
       transport and dispersion model."""

    homepage = "https://www.flexpart.eu"
    git      = "https://www.flexpart.eu/gitmob/flexpart"

    maintainers = ['barche', 'tcarion']

    version('10.4', tag='v10.4')

    depends_on('netcdf-fortran')
    depends_on('grib-api+fortran fflags="-fallow-argument-mismatch"')
    depends_on('jasper')

    build_directory = 'src'

    def edit(self, spec, prefix):
        makefile = FileFilter('src/makefile')
        gribinc = self.spec['grib-api'].prefix.include
        makefile.filter('INCPATH1 += .*',  'INCPATH1 = {0}'.format(gribinc))
        makefile.filter('F90.*= .*',  'F90 = f90')
        makefile.filter('MPIF90.*= .*',  'MPIF90 = mpif90')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('src/FLEXPART', prefix.bin)
