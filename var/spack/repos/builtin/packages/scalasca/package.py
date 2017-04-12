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


class Scalasca(AutotoolsPackage):
    """Scalasca is a software tool that supports the performance optimization
       of parallel programs by measuring and analyzing their runtime
       behavior. The analysis identifies potential performance
       bottlenecks - in particular those concerning communication and
       synchronization - and offers guidance in exploring their causes.

    """

    homepage = "http://www.scalasca.org"
    url = "http://apps.fz-juelich.de/scalasca/releases/scalasca/2.1/dist/scalasca-2.1.tar.gz"

    version('2.3.1', 'a83ced912b9d2330004cb6b9cefa7585')
    version('2.2.2', '2bafce988b0522d18072f7771e491ab9')
    version('2.1',   'bab9c2b021e51e2ba187feec442b96e6')

    depends_on("mpi")
    ##########
    # Hard-code dependencies for Scalasca according to what stated in the
    # release page
    # The OTF2 library path should be detected automatically from SCOREP
    # SCALASCA 2.2.2
    depends_on("scorep@1.4:", when='@2.2.2:')
    # Use same cube as scorep does
    # -> depends_on("cube@4.3:", when='@2.2.2:')
    # SCALASCA 2.1
    depends_on("scorep@1.3", when='@2.1')
    # Use same cube as scorep does
    # -> depends_on("cube@4.2:", when='@2.1')
    ##########

    def url_for_version(self, version):
        return 'http://apps.fz-juelich.de/scalasca/releases/scalasca/{0}/dist/scalasca-{1}.tar.gz'.format(version.up_to(2), version)

    def configure_args(self):
        spec = self.spec

        config_args = ["--enable-shared"]

        if 'cube' in spec:  # From scorep dependency
            config_args.append("--with-cube=%s" % spec['cube'].prefix.bin)

        return config_args
