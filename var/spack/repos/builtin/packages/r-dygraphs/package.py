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


class RDygraphs(Package):
    """An R interface to the 'dygraphs' JavaScript charting library (a copy of
    which is included in the package). Provides rich facilities for charting
    time-series data in R, including highly configurable series- and
    axis-display and interactive features like zoom/pan and series/point
    highlighting."""

    homepage = "https://cran.r-project.org/web/packages/dygraphs/index.html"
    url      = "https://cran.r-project.org/src/contrib/dygraphs_0.9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/dygraphs"

    version('0.9', '7f0ce4312bcd3f0a58b8c03b2772f833')

    extends('R')

    depends_on('r-magrittr', type=nolink)
    depends_on('r-htmlwidgets', type=nolink)
    depends_on('r-zoo', type=nolink)
    depends_on('r-xts', type=nolink)

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)
