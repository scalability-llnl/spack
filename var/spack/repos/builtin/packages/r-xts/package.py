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


class RXts(Package):
    """Provide for uniform handling of R's different time-based data classes by
    extending zoo, maximizing native format information preservation and
    allowing for user level customization and extension, while simplifying
    cross-class interoperability."""

    homepage = "http://r-forge.r-project.org/projects/xts/"
    url      = "https://cran.r-project.org/src/contrib/xts_0.9-7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/xts"

    version('0.9-7', 'a232e94aebfa654653a7d88a0503537b')

    extends('R')

    depends_on('r-zoo', type=nolink)

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)
