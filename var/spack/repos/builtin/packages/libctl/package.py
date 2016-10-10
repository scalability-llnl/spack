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


class Libctl(Package):
    """libctl is a free Guile-based library implementing flexible
    control files for scientific simulations."""

    homepage = "http://ab-initio.mit.edu/wiki/index.php/Libctl"
    url      = "http://ab-initio.mit.edu/libctl/libctl-3.2.2.tar.gz"

    version('3.2.2', '5fd7634dc9ae8e7fa70a68473b9cbb68')

    depends_on('guile')

    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix),
                  '--enable-shared',
                  'GUILE={0}'.format(join_path(
                      spec['guile'].prefix.bin, 'guile')),
                  'GUILE_CONFIG={0}'.format(join_path(
                      spec['guile'].prefix.bin, 'guile-config')))

        make()
        make('install')
