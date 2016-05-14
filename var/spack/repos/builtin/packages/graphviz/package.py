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

class Graphviz(Package):
    """Graph Visualization Software"""
    homepage = "http://www.graphviz.org"
    url      = "http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.38.0.tar.gz"

    version('2.38.0', '5b6a829b2ac94efcd5fa3c223ed6d3ae')

    # By default disable optional Perl language support to prevent build issues
    # related to missing Perl packages. If spack begins support for Perl in the
    # future, this package can be updated to depend_on('perl') and the
    # ncecessary devel packages.
    variant('perl', default=False, description='Enable if you need the optional Perl language bindings.')

    parallel = False

    depends_on("swig")
    depends_on("python")
    depends_on("ghostscript")

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix]
        if not '+perl' in spec:
            options.append('--disable-perl')

        configure(*options)
        make()
        make("install")
