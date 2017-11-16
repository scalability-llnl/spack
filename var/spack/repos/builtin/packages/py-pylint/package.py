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


class PyPylint(PythonPackage):
    """array processing for numbers, strings, records, and objects."""
    homepage = "https://pypi.python.org/pypi/pylint"
    url      = "https://pypi.io/packages/source/p/pylint/pylint-1.7.2.tar.gz"

    version('1.7.2', '27ee752cdcfacb05bf4940947e6b35c6')
    version('1.4.3', '5924c1c7ca5ca23647812f5971d0ea44')
    version('1.4.1', 'df7c679bdcce5019389038847e4de622')

    extends('python', ignore=r'bin/pytest')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-astroid', type=('build', 'run'))
    depends_on('py-logilab-common', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    # TODO: Add a 'test' deptype
    # depends_on('py-nose', type='test')
