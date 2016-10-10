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


class RGgmap(Package):
    """A collection of functions to visualize spatial data and models on top of
    static maps from various online sources (e.g Google Maps and Stamen Maps).
    It includes tools common to those tasks, including functions for
    geolocation and routing."""

    homepage = "https://github.com/dkahle/ggmap"
    url      = "https://cran.r-project.org/src/contrib/ggmap_2.6.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ggmap"

    version('2.6.1', '25ad414a3a1c6d59a227a9f22601211a')

    extends('R')

    depends_on('r-ggplot2', type=nolink)
    depends_on('r-proto', type=nolink)
    depends_on('r-rgooglemaps', type=nolink)
    depends_on('r-png', type=nolink)
    depends_on('r-plyr', type=nolink)
    depends_on('r-reshape2', type=nolink)
    depends_on('r-rjson', type=nolink)
    depends_on('r-mapproj', type=nolink)
    depends_on('r-jpeg', type=nolink)
    depends_on('r-geosphere', type=nolink)
    depends_on('r-digest', type=nolink)
    depends_on('r-scales', type=nolink)

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)
