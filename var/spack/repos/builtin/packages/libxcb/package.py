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


class Libxcb(AutotoolsPackage):
    """The X protocol C-language Binding (XCB) is a replacement
    for Xlib featuring a small footprint, latency hiding, direct
    access to the protocol, improved threading support, and
    extensibility."""

    homepage = "https://xcb.freedesktop.org/"
    url      = "https://xcb.freedesktop.org/dist/libxcb-1.11.tar.gz"

    version('1.12', '95eee7c28798e16ba5443f188b27a476')
    version('1.11', '1698dd837d7e6e94d029dbe8b3a82deb')
    version('1.11.1', '118623c15a96b08622603a71d8789bf3')

    depends_on('libpthread-stubs')
    depends_on('libxau@0.99.2:')
    depends_on('libxdmcp')

    depends_on('xcb-proto', type='build')
    depends_on('python@2:2.8', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def patch(self):
        filter_file(
            'typedef struct xcb_auth_info_t {',
            'typedef struct {',
            'src/xcb.h')
