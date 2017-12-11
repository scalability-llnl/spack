##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class PyMethylcode(PythonPackage):
    """MethylCoder is a single program that takes of bisulfite-treated
       reads and outputs per-base methylation data. """

    homepage = "https://github.com/brentp/methylcode"
    url      = "https://github.com/brentp/methylcode/archive/master.zip"

    version('1.0.0', 'd0ba07c1ab2c74adddd1b23f8e5823e7')

    depends_on('python@2.7.0:2.7.999')
    depends_on('py-six')
    depends_on('py-setuptools')
    depends_on('py-numpy')
    depends_on('py-pyparsing')
    depends_on('py-pyfasta')
    depends_on('py-bsddb3')
    depends_on('bowtie')
