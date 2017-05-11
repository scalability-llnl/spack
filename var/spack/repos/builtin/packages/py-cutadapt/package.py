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


class PyCutadapt(PythonPackage):
    """Cutadapt finds and removes adapter sequences, primers, poly-A tails and other types of unwanted sequence from your high-throughput sequencing reads."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://cutadapt.readthedocs.io"
    url      = "https://pypi.python.org/packages/4b/a0/caf0a418d64a69da12c0f5ede20830f0b7dba2d29efa3f667f1ce69e78da/cutadapt-1.13.tar.gz#md5=2d2d14e0c20ad53d7d84b57bc3e63b4c"

    version('1.13', '2d2d14e0c20ad53d7d84b57bc3e63b4c')

    depends_on('py-setuptools',        type=('build'))
    depends_on('py-xopen',        type=('run'))
    depends_on('py-six',        type=('run'))
    depends_on('py-packaging',        type=('run'))
    depends_on('py-pyparsing',        type=('run'))
    depends_on('py-appdirs',        type=('run'))
