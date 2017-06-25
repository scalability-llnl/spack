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


class OctaveSplines(Package):
    """Additional spline functions."""

    homepage = "http://octave.sourceforge.net/splines/index.html"
    url      = "http://downloads.sourceforge.net/octave/splines-1.3.1.tar.gz"

    version('1.3.1', 'f9665d780c37aa6a6e17d1f424c49bdeedb89d1192319a4e39c08784122d18f9')

    extends('octave@3.6.0:')

    def install(self, spec, prefix):
        octave('--quiet',
               '--norc',
               '--built-in-docstrings-file=/dev/null',
               '--texi-macros-file=/dev/null',
               '--eval', 'pkg prefix %s; pkg install %s' %
               (prefix, self.stage.archive_file))
