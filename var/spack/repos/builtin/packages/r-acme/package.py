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


class RAcme(RPackage):
    """ACME (Algorithms for Calculating Microarray Enrichment) is a set
    of tools for analysing tiling array ChIP/chip, DNAse hypersensitivity,
    or other experiments that result in regions of the genome showing
    "enrichment". It does not rely on a specific array technology
    (although the array should be a "tiling" array), is very general
    (can be applied in experiments resulting in regions of enrichment),
    and is very insensitive to array noise or normalization methods.
    It is also very fast and can be applied on whole-genome tiling array
    experiments quite easily with enough memory."""

    homepage = "https://www.bioconductor.org/packages/ACME/"
    url      = "https://www.bioconductor.org/packages/release/bioc/src/contrib/ACME_2.32.0.tar.gz"

    version('2.32.0', 'f99ea6b94399fd7a10f55ac7e7ec04fa')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
