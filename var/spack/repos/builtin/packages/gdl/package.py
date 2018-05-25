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
from spack import *


class Gdl(CMakePackage):
    """A free and open-source IDL/PV-WAVE compiler

    GNU Data Language (GDL) is a free/libre/open source incremental compiler
    compatible with IDL and to some extent with PV-WAVE.
    """

    homepage = "https://github.com/gnudatalanguage/gdl"
    url      = "https://github.com/gnudatalanguage/gdl/archive/v0.9.8.tar.gz"

    version('0.9.8', '447b0362e1df5ea8af814a969e89d3ec')

    variant('python', default=False)
    variant('x11', default=False)
    variant('proj', default=True)
    variant('graphicsmagick', default=False)

    extends('python', when='+python')

    depends_on('python@2.7:2.8', type=('build', 'run'), when='+python')
    depends_on('py-numpy', type=('build', 'run'), when='+python')
    depends_on('libx11', when='+x11')
    depends_on('proj', when='+proj')
    depends_on('graphicsmagick', when='+graphicsmagick')
    depends_on('plplot')
    depends_on('gsl')
    depends_on('readline')
    depends_on('netcdf')
    depends_on('jpeg')
    depends_on('hdf5')
    depends_on('hdf')
    depends_on('fftw')
    depends_on('eigen')
    depends_on('pslib')

    def cmake_args(self):
        args = []
        # wxWidgets isn't packaged yet
        args += ['-DWXWIDGETS=OFF']
        # only version 6 of ImageMagick is supported and version 7 is packaged
        args += ['-DMAGICK=OFF']

        if '+graphicsmagick' not in self.spec:
            args += ['-DGRAPHICSMAGICK=OFF']

        if '+python' not in self.spec:
            args += ['-DPYTHON=OFF']

        if '+proj' in self.spec:
            args += [
                '-DLIBPROJ4=YES',
                '-DLIBPROJ4DIR={0}'.format(self.spec['proj'].prefix)
            ]

        return args
