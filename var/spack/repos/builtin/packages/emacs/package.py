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


class Emacs(AutotoolsPackage):
    """The Emacs programmable text editor."""

    homepage = "https://www.gnu.org/software/emacs"
    url      = "http://ftp.gnu.org/gnu/emacs/emacs-25.1.tar.gz"

    version('25.1', '95c12e6a9afdf0dcbdd7d2efa26ca42c')
    version('24.5', 'd74b597503a68105e61b5b9f6d065b44')

    variant('X', default=False, description="Enable an X toolkit")
    variant('gui', default=None,
                description='GUI toolkit to use (requires X11)',
                values=('gtk', 'athena'))

    depends_on('ncurses')
    depends_on('libtiff', when='+X')
    depends_on('libpng', when='+X')
    depends_on('libxpm', when='+X')
    depends_on('giflib', when='+X')
    depends_on('libx11', when='+X')
    depends_on('libxaw', when='gui=athena')
    depends_on('gtkplus+X', when='gui=gtk')

    def configure_args(self):
        spec = self.spec
        args = []
        if self.variants['gui'].value is None:
            args = ['--without-x',
                    '--with-jpeg=no',
                    '--with-gif=no',
                    '--with-tiff=no',
                    '--with-xpm=no',
                    '--with-x-toolkit=no',
                    ]
        else:
            args = [
                '--with-x',
                '--with-x-toolkit={0}'.format(spec.variants['gui'].value)
            ]

        return args
