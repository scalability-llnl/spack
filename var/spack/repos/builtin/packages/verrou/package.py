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
from spack import *
import os
import sys


class Verrou(AutotoolsPackage):
    """A floating-point error checker.

    Verrou helps you look for floating-point round-off errors in programs. It
    implements a stochastic floating-point arithmetic based on random rounding:
    all floating-point operations are perturbed by randomly switching rounding
    modes. This can be seen as an asynchronous variant of the CESTAC method, or
    a subset of Monte Carlo Arithmetic, performing only output randomization
    through random rounding.
    """

    homepage = "https://github.com/edf-hpc/verrou"
    url      = "https://github.com/edf-hpc/verrou.git"

    version('master',
            git='https://github.com/edf-hpc/verrou.git',
            branch='master')

    version('2.0.0',
            git='https://github.com/edf-hpc/verrou.git',
            commit='a614ad695d060abdfcd3cec11022d6f044a0980d')
    version('1.1.0',
            git='https://github.com/edf-hpc/verrou.git',
            commit='d69787e89507519e14f5ec44150c1882930f692e')
    version('1.0.0',
            git='https://github.com/edf-hpc/verrou.git',
            commit='519dd9a83738f72da8446322e9c403e608940b7a')
    version('0.9.0',
            git='https://github.com/edf-hpc/verrou.git',
            commit='ebabfcf7f4e9a02b130e9819ba6c19e0450eb73d')

    resource(name='valgrind-3.13.0',
             git='git://sourceware.org/git/valgrind.git',
             commit='1378ec95f22235e0a8c972cf1cd0abef0b9610d4',
             when='@1.1.0:,master')
    resource(name='valgrind-3.12.0',
             git='git://sourceware.org/git/valgrind.git',
             commit='36923ab298c8d2791d6c86b6cd5c0667c07449f6',
             when='@1.0.0:1.0.999')
    resource(name='valgrind-3.10.1',
             git='git://sourceware.org/git/valgrind.git',
             commit='cfc3175a6eb132a5600fcf705f3fa326d71483bf',
             when='@0.9.0:0.9.999')

    conflicts('valgrind')

    variant('fma', default=True,
            description='Activates fused multiply-add support for Verrou')

    def patch(self):
        # The current setup gives us the verrou source tree, with a "valgrind"
        # subdirectory. But we want the reverse layout. Let's fix this.
        verrou_files = os.listdir('.')
        verrou_files.remove('valgrind')
        os.mkdir('verrou')
        for name in verrou_files:
            os.rename(name, os.path.join('verrou', name))
        for name in os.listdir('valgrind'):
            os.rename(os.path.join('valgrind', name), name)
        os.rmdir('valgrind')

        # Once this is done, we can patch valgrind
        which('patch')('-p0', '--input=verrou/valgrind.diff')

    def autoreconf(self, spec, prefix):
        # Needed because we patched valgrind
        which("bash")("autogen.sh")

    def configure_args(self):
        spec = self.spec
        options = ['--enable-only64bit']

        if spec.satisfies('+fma'):
            options.append('--enable-verrou-fma')

        if sys.platform == 'darwin':
            options.append('--build=amd64-darwin')

        return options
