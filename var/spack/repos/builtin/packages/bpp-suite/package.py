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


class BppSuite(Package):
    """BppSuite is a suite of ready-to-use programs for phylogenetic and
       sequence analysis."""

    homepage = "http://biopp.univ-montp2.fr/wiki/index.php/BppSuite"
    url      = "http://biopp.univ-montp2.fr/repos/sources/bppsuite/bppsuite-2.2.0.tar.gz"

    version('2.2.0', 'd8b29ad7ccf5bd3a7beb701350c9e2a4')

    depends_on('cmake', type='build')
    depends_on('texinfo', type='build')
    depends_on('bpp-core')
    depends_on('bpp-seq')
    depends_on('bpp-phyl')

    def install(self, spec, prefix):
        cmake('.', *std_cmake_args)
        make()
        make('install')
