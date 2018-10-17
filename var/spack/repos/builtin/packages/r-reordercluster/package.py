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


class RReordercluster(RPackage):
    """Tools for performing the leaf reordering for the dendrogram
    that preserves the hierarchical clustering result and at the
    same time tries to group instances from the same class together."""

    homepage = "https://cran.r-project.org/package=ReorderCluster"
    url      = "https://cran.rstudio.com/src/contrib/ReorderCluster_1.0.tar.gz"

    version('1.0', sha256='a87898faa20380aac3e06a52eedcb2f0eb2b35ab74fdc3435d40ee9f1d28476b')

    depends_on('r-gplots', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
