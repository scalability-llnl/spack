##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class Cube(Package):
    """
    Cube the profile viewer for Score-P and Scalasca profiles. It displays a multi-dimensional performance space
    consisting of the dimensions:
    - performance metric
    - call path
    - system resource
    """

    homepage = "http://www.scalasca.org/software/cube-4.x/download.html"
    url = "http://apps.fz-juelich.de/scalasca/releases/cube/4.2/dist/cube-4.2.3.tar.gz"

    version('4.3.3', '07e109248ed8ffc7bdcce614264a2909',
            url='http://apps.fz-juelich.de/scalasca/releases/cube/4.3/dist/cube-4.3.3.tar.gz')

    version('4.2.3', '8f95b9531f5a8f8134f279c2767c9b20',
            url="http://apps.fz-juelich.de/scalasca/releases/cube/4.2/dist/cube-4.2.3.tar.gz")

    # TODO : add variant that builds GUI on top of Qt

    def install(self, spec, prefix):
        configure_args = ["--prefix=%s" % prefix,
                          "--without-paraver",
                          "--without-gui"]
        configure(*configure_args)
        make(parallel=False)
        make("install", parallel=False)
