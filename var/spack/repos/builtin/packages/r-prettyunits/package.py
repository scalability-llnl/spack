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


class RPrettyunits(RPackage):
    """Pretty, human readable formatting of quantities. Time intervals:
       1337000 -> 15d 11h 23m 20s. Vague time intervals: 2674000 -> about
       a month ago. Bytes: 1337 -> 1.34 kB."""

    homepage = "https://cran.r-project.org/package=prettyunits"
    url      = "https://cran.r-project.org/src/contrib/prettyunits_1.0.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/prettyunits"

    version('1.0.2', '0a091a297e8b37df54e7fcf28697ee50')

    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
