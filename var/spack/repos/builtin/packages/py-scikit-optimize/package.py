##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-scikit-optimize
#
# You can edit this file again by typing:
#
#     spack edit py-scikit-optimize
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class PyScikitOptimize(PythonPackage):
    """Scikit-Optimize, or skopt, is a simple and efficient library to minimize (very) expensive 
    and noisy black-box functions. It implements several methods for sequential model-based optimization."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://scikit-optimize.github.io/"
    url      = "https://github.com/scikit-optimize/scikit-optimize/archive/v0.5.2.tar.gz"

    version('0.5.2', sha256='f2cba57e20787a24c6d18d8ae1505838f0e9ea7594f1f3b12cdf8e97348752a7')

    # FIXME: Add dependencies if required.
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-nose', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
