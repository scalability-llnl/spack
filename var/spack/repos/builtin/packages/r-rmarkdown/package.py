##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class RRmarkdown(RPackage):
    """Convert R Markdown documents into a variety of formats."""

    homepage = "http://rmarkdown.rstudio.com/"
    url      = "https://cran.r-project.org/src/contrib/rmarkdown_1.0.tar.gz"

    version('1.0', '264aa6a59e9680109e38df8270e14c58')

    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-catools', type=('build', 'run'))
    depends_on('r-evaluate', type=('build', 'run'))
    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
