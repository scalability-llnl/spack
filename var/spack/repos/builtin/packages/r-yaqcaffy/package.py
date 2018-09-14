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


class RYaqcaffy(RPackage):
    """Quality control of Affymetrix GeneChip expression data and
       reproducibility analysis of human whole genome chips with the MAQC
       reference datasets."""

    homepage = "http://bioconductor.org/packages/yaqcaffy/"
    git      = "https://git.bioconductor.org/packages/yaqcaffy.git"

    version('1.36.0', commit='4d46fe77b2c8de2230a77b0c07dd5dd726e3abd6')

    depends_on('r-simpleaffy', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.36.0')
