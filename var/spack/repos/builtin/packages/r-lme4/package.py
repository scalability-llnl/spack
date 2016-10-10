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


class RLme4(Package):
    """Fit linear and generalized linear mixed-effects models. The models and
    their components are represented using S4 classes and methods. The core
    computational algorithms are implemented using the 'Eigen' C++ library for
    numerical linear algebra and 'RcppEigen' "glue"."""

    homepage = "https://github.com/lme4/lme4/"
    url      = "https://cran.r-project.org/src/contrib/lme4_1.1-12.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/lme4"

    version('1.1-12', 'da8aaebb67477ecb5631851c46207804')

    extends('R')

    depends_on('r-matrix', type=nolink)
    depends_on('r-mass', type=nolink)
    depends_on('r-lattice', type=nolink)
    depends_on('r-nlme', type=nolink)
    depends_on('r-minqa', type=nolink)
    depends_on('r-nloptr', type=nolink)
    depends_on('r-rcpp', type=nolink)
    depends_on('r-rcppeigen', type=nolink)

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)
