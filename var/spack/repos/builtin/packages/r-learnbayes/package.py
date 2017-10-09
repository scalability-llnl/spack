##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class RLearnbayes(RPackage):
    """LearnBayes contains a collection of functions helpful in learning the
    basic tenets of Bayesian statistical inference. It contains functions for
    summarizing basic one and two parameter posterior distributions and
    predictive distributions. It contains MCMC algorithms for summarizing
    posterior distributions defined by the user. It also contains functions
    for regression models, hierarchical models, Bayesian tests, and
    illustrations of Gibbs sampling."""

    homepage = "https://CRAN.R-project.org/package=LearnBayes"
    url      = "https://cran.r-project.org/src/contrib/LearnBayes_2.15.tar.gz"

    version('2.15', '213713664707bc79fd6d3a109555ef76')
