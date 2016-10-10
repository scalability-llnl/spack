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


class RQuantreg(Package):
    """Estimation and inference methods for models of conditional quantiles:
        Linear and nonlinear parametric and non-parametric (total variation
        penalized) models for conditional quantiles of a univariate response
        and several methods for handling censored survival data. Portfolio
        selection methods based on expected shortfall risk are also
        included."""

    homepage = "https://cran.r-project.org/package=quantreg"
    url      = "https://cran.r-project.org/src/contrib/quantreg_5.26.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/quantreg"

    version('5.26', '1d89ed932fb4d67ae2d5da0eb8c2989f')

    extends('R')

    depends_on('r-sparsem', type=nolink)
    depends_on('r-matrix', type=nolink)
    depends_on('r-matrixmodels', type=nolink)

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)
