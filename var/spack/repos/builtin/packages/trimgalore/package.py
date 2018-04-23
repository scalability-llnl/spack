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


class Trimgalore(Package):
    """Trim Galore! is a wrapper around Cutadapt and FastQC to consistently
       apply adapter and quality trimming to FastQ files, with extra
       functionality for RRBS data."""

    homepage = "https://github.com/FelixKrueger/TrimGalore"
    url      = "https://github.com/FelixKrueger/TrimGalore/archive/0.4.4.tar.gz"

    version('0.4.5', 'c71756042b2a65c34d483533a29dc206')
    version('0.4.4', 'aae1b807b48e38bae7074470203997bb')

    depends_on('perl', type=('build', 'run'))
    depends_on('py-cutadapt', type=('build', 'run'))
    depends_on('fastqc')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('trim_galore', prefix.bin)
