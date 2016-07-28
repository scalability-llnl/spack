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


class Pdt(Package):
    """
    Program Database Toolkit (PDT) is a framework for analyzing source code written in several programming languages
    and for making rich program knowledge accessible to developers of static and dynamic analysis tools. PDT implements
    a standard program representation, the program database (PDB), that can be accessed in a uniform way through a
    class library supporting common PDB operations.
    """
    homepage = "https://www.cs.uoregon.edu/research/pdt/home.php"
    url      = "https://www.cs.uoregon.edu/research/tau/pdt_releases/pdt-3.21.tar.gz"

    version('3.21', '8df94298b71703decf680709a4ddf68f')
    version('3.19', 'ba5591994998771fdab216699e362228')

    def install(self, spec, prefix):
        configure('-prefix=%s' % prefix)
        make()
        make("install")
