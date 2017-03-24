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


class PyDev(PythonPackage):
    """libraries and tools for Python development"""

    homepage = "https://pypi.python.org/pypi/dev"
    url      = "https://pypi.python.org/packages/53/34/e0d4da6c3e9ea8fdcc4657699f2ca62d5c4ac18763a897feb690c2fb0574/dev-0.4.0.tar.gz"

    version('0.4.0', '00449cf0b347c32da9c840adcb4cf24b')

    patch('__init__.py.patch')

    depends_on('py-setuptools', type='build')
