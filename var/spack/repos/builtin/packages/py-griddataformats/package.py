##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class PyGriddataformats(PythonPackage):
    """The gridDataFormats package provides classes to unify reading
    and writing n-dimensional datasets. One can read grid data from
    files, make them available as a Grid object, and write out the
    data again."""

    homepage = "http://www.mdanalysis.org/GridDataFormats"
    url      = "https://pypi.io/packages/source/G/GridDataFormats/GridDataFormats-0.3.3.tar.gz"

    version('0.3.3', '5c83d3bdd421eebcee10111942c5a21f')

    depends_on('python@2.7:')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.0.3:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
