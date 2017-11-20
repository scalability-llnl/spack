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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install gotcha
#
# You can edit this file again by typing:
#
#     spack edit gotcha
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Gotcha(CMakePackage):
    """C software library for shared library function wrapping, 
    enables tools to intercept calls into shared libraries"""

    homepage = "http://github.com/LLNL/gotcha"
    url      = "http://github.com/LLNL/gotcha"

    variant('test', default=False, description='Build tests for Gotcha')

    # FIXME: Add proper versions and checksums here.
    version('develop', git='https://github.com/LLNL/gotcha.git', branch="develop")
    version('master', git='https://github.com/LLNL/gotcha.git', branch="master")
    version('0.0.2', git='https://github.com/LLNL/gotcha.git', tag="0.0.2")

    def configure_args(self):
        spec = self.spec
        return [
            '-DGOTCHA_ENABLE_TESTS=%s' % ('ON' if '+test' in spec else 'OFF')
        ]
