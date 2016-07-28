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
import os

class Spot(Package):
    """Spot is a C++11 library for omega-automata manipulation and model checking."""
    homepage = "https://spot.lrde.epita.fr/index.html"
    url      = "http://www.lrde.epita.fr/dload/spot/spot-1.99.3.tar.gz"

    version('1.99.3', 'd53adcb2d0fe7c69f45d4e595a58254e')

    #depends_on("gcc@4.8:", type='build')
    depends_on("python@3.2:")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
