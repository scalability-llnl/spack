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
#
from spack import *


class PyParamiko(PythonPackage):
    """SSH2 protocol library"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://pypi.python.org/pypi/paramiko/2.1.2"
    url      = "https://pypi.python.org/packages/64/79/5e8baeedb6baf1d5879efa8cd012f801efc232e56a068550ba00d7e82625/paramiko-2.1.2.tar.gz#md5=41a8ea0e8abb03a6bf59870670d4f46c"

    version('2.1.2', '41a8ea0e8abb03a6bf59870670d4f46c')

    depends_on('py-setuptools', type=('build', 'link'))
    depends_on('py-pyasn1',        type=('build', 'run'))
    depends_on('py-cryptography',  type=('build', 'link', 'run'))

