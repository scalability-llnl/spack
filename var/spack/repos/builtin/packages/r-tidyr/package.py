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


class RTidyr(Package):
    """An evolution of 'reshape2'. It's designed specifically for data tidying
    (not general reshaping or aggregating) and works well with 'dplyr' data
    pipelines."""

    homepage = "https://github.com/hadley/tidyr"
    url      = "https://cran.r-project.org/src/contrib/tidyr_0.5.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/tidyr"

    version('0.5.1', '3cadc869510c054ed93d374ab44120bd')

    extends('R')
    depends_on('r-tibble', type=nolink)
    depends_on('r-dplyr', type=nolink)
    depends_on('r-stringi', type=nolink)
    depends_on('r-lazyeval', type=nolink)
    depends_on('r-magrittr', type=nolink)
    depends_on('r-rcpp', type=nolink)

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)
