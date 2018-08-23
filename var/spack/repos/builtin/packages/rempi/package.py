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


class Rempi(AutotoolsPackage):
    """ReMPI is a record-and-replay tool for MPI applications."""
    homepage = "https://github.com/PRUNERS/ReMPI"
    url      = "https://github.com/PRUNERS/ReMPI/releases/download/v1.0.0/ReMPI-1.0.0.tar.gz"

    version("1.1.0", "05b872a6f3e2f49a2fc6112a844c7f43")
    version("1.0.0", "32c780a6a74627b5796bea161d4c4733")

    depends_on("mpi")
    depends_on("zlib")
    depends_on("autoconf", type='build')
    depends_on("automake", type='build')
    depends_on("libtool", type='build')
