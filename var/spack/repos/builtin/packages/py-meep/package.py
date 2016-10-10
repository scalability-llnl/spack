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


class PyMeep(Package):
    """Python-meep is a wrapper around libmeep. It allows the scripting of
    Meep-simulations with Python"""

    homepage = "https://launchpad.net/python-meep"
    url      = "https://launchpad.net/python-meep/1.4/1.4/+download/python-meep-1.4.2.tar"

    version('1.4.2', 'f8913542d18b0dda92ebc64f0a10ce56')

    variant('mpi', default=True, description='Enable MPI support')

    extends('python')
    depends_on('py-numpy', type=nolink)
    depends_on('py-scipy', type=nolink)
    depends_on('py-matplotlib', type=nolink)

    depends_on('mpi', when='+mpi')
    depends_on('meep~mpi', when='~mpi')
    depends_on('meep+mpi', when='+mpi')

    # As of SWIG 3.0.3, Python-style comments are now treated as
    # pre-processor directives. Use older SWIG. But not too old,
    # or else it can't handle newer C++ compilers and flags.
    depends_on('swig@1.3.39:3.0.2')

    def install(self, spec, prefix):
        setup = 'setup-mpi.py' if '+mpi' in spec else 'setup.py'

        include_dirs = [
            spec['meep'].prefix.include,
            spec['py-numpy'].include
        ]

        library_dirs = [
            spec['meep'].prefix.lib
        ]

        if '+mpi' in spec:
            include_dirs.append(spec['mpi'].prefix.include)
            library_dirs.append(spec['mpi'].prefix.lib)

        include_flags = '-I{0}'.format(','.join(include_dirs))
        library_flags = '-L{0}'.format(','.join(library_dirs))

        python(setup, 'clean', '--all')
        python(setup, 'build_ext', include_flags, library_flags)
        python(setup, 'install', '--prefix={0}'.format(prefix))
        python(setup, 'bdist', include_flags, library_flags)
