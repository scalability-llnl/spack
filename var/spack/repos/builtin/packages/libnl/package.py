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
import sys


class Libnl(AutotoolsPackage):
    """libnl - Netlink Protocol Library Suite"""

    homepage = "https://www.infradead.org/~tgr/libnl/"
    url      = "https://github.com/thom311/libnl/releases/download/libnl3_3_0/libnl-3.3.0.tar.gz"

    version('3.3.0', 'ab3ef137cad95bdda5ff0ffa5175dfa5')
    version('3.2.25', '03f74d0cd5037cadc8cdfa313bbd195c')

    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('m4', type='build')

    @run_before('autoreconf')
    def check_platform(self):
        if not (sys.platform.startswith('freebsd') or
                sys.platform.startswith('linux')):
            raise InstallError("libnl requires FreeBSD or Linux")
