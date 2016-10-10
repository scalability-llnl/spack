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


class Libxau(Package):
    """The libXau package contains a library implementing the X11
       Authorization Protocol. This is useful for restricting client
       access to the display."""
    homepage = "http://xcb.freedesktop.org/"
    url      = "http://ftp.x.org/pub/individual/lib/libXau-1.0.8.tar.bz2"

    version('1.0.8', '685f8abbffa6d145c0f930f00703b21b')

    depends_on('xproto')
    depends_on('pkg-config', type='build')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
