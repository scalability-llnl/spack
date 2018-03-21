##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Libx11(AutotoolsPackage):
    """libX11 - Core X11 protocol client library."""

    homepage = "https://www.x.org/"
    url      = "https://www.x.org/archive/individual/lib/libX11-1.6.5.tar.gz"

    version('1.6.5', '300b5831916ffcc375468431d856917e')
    version('1.6.3', '7d16653fe7c36209799175bb3dc1ae46')

    depends_on('libxcb@1.1.92:')

    depends_on('xproto@7.0.17:', type='include')
    depends_on('xextproto', type=('build', 'link'))
    depends_on('xtrans', type='build')
    depends_on('kbproto', type=('build', 'link'))
    depends_on('inputproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
    depends_on('perl', type='build')
