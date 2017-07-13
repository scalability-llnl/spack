##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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


class REvaluate(RPackage):
    """Parsing and evaluation tools that make it easy to recreate the command
    line behaviour of R."""

    homepage = "https://github.com/hadley/evaluate"
    url      = "https://cran.rstudio.com/src/contrib/evaluate_0.9.tar.gz"

    version('0.10', 'c49326babf984a8b36e7e276da370ad2')
    version('0.9',  '877d89ce8a9ef7f403b1089ca1021775')

    depends_on('r@3.0.2:')

    depends_on('r-stringr@0.6.2:', type=('build', 'run'))
