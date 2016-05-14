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

class Ncview(Package):
    """Simple viewer for NetCDF files."""
    homepage = "http://meteora.ucsd.edu/~pierce/ncview_home_page.html"
    url      = "ftp://cirrus.ucsd.edu/pub/ncview/ncview-2.1.7.tar.gz"

    version('2.1.7', 'debd6ca61410aac3514e53122ab2ba07')

    depends_on("netcdf")
    depends_on("udunits2")

    # OS Dependencies
    # Ubuntu: apt-get install libxaw7-dev
    # CentOS 7: yum install libXaw-devel

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make("install")
