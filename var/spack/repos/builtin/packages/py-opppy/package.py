##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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
import os


class PyOpppy(PythonPackage):
    """The Output Parse-Plot Python (OPPPY) library is a python based data
    analysis library designed to extract, store, and plot information from
    output and dump files generated by scientific software packages."""

    homepage = "https://github.com/lanl/opppy"
    url = "https://github.com/lanl/OPPPY/archive/OPPPY-0_1_1.tar.gz"
    git = "https://github.com/lanl/opppy.git"

    version('master', branch='master')
    version('0.1.1', '852a1329ce68d678623beed3fd01ea98')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy@1.6:', type=('build', 'run'))
    depends_on('python@3:',     type=('build', 'run'))
    depends_on('py-argparse',   type=('build', 'run'))
    depends_on('py-scipy',      type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-sphinx',     type=('build', 'run'))
