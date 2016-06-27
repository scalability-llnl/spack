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

class Xproto(Package):
    """The Xorg protocol headers provide the header files required to
       build the system, and to allow other applications to build against
       the installed X Window system."""
    homepage = "http://www.x.org/"
    url      = "https://www.x.org/archive//individual/proto/xproto-7.0.29.tar.gz"

    version('7.0.29', '16a78dd2c5ad73011105c96235f6a0af')

    depends_on("xorg-util-macros")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make("install")
