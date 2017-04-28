##############################################################################
# Copyright (c) 2017, The VOTCA Development Team (http://www.votca.org)
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


class VotcaCsg(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the VOTCA coarse-graining engine.
    """
    homepage = "http://www.votca.org"
    url      = "https://github.com/votca/csg/tarball/v1.4"

    version('develop', git='https://github.com/csg/tools', branch='master')
    version('1.4', 'd009e761e5e3afd51eed89c420610a67')

    variant('debug', default=False, description='Build debug version')

    depends_on("cmake@2.8:", type='build')
    depends_on("votca-tools")
    depends_on("gromacs@5.1:")

    def build_type(self):
        spec = self.spec
        if '+debug' in spec:
            return 'Debug'
        else:
            return 'Release'
