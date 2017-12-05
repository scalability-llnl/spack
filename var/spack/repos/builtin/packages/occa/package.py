##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Serban Maerean, serban@us.ibm.com, All rights reserved.
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
import os
import shutil
import sys

from spack import *


class Occa(MakefilePackage):
    """
    OCCA is an open-source library that facilitates programming in an environment
    containing different types of devices. We abstract devices and let the user
    pick at run-time, for example: CPUs, GPUs, Intel's Xeon Phi, FPGAs.
    """

    homepage = "http://libocca.org"
    url      = "https://github.com/libocca/occa/archive/0.1.tar.gz"

    version('0.1', 'bb042c251cdc4c68b897eaf6a43cdd26')

    variant('openmp', default=False,
            description="Enable OpenMP backend")
    variant('opencl', default=False,
            description="Enable OpenCL backend")
    variant('cuda'  , default=False,
            description="Enable CUDA backend")

    depends_on('cuda'  , when='+cuda')
    depends_on('opencl', when='+opencl')

    def install(self, spec, prefix):
        make()
        try:
            os.makedirs(prefix)
        except OSError:
            pass
        for path in ['bin', 'include', 'lib', 'scripts']:
            shutil.copytree('{}'.format(path),
                            '{}/{}'.format(prefix, path))
