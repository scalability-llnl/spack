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
import glob
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
    url      = "https://github.com/edf-hpc/verrou/archive/v2.0.0.tar.gz"

    version('develop',
            git='https://github.com/edf-hpc/verrou.git',
            branch='master')

    version('2.0.0', '388d493df3f253c9b049ce0ceae55fd6')
    version('1.1.0', '9752d776fb534890e5e29f9721ee6125')
    version('1.0.0', '01e90416aa4ac0dbde9bd165afe4cbfe')
    version('0.9.0', '42d69fc7dbdc7c374a14375084f72392')

    resource(name='valgrind-3.13.0',
             url='https://sourceware.org/pub/valgrind/valgrind-3.13.0.tar.bz2',
             sha256='d76680ef03f00cd5e970bbdcd4e57fb1f6df7d2e2c071635ef2be74790190c3b',
             when='@1.1.0:,master')
    resource(name='valgrind-3.13.0',
             url='https://sourceware.org/pub/valgrind/valgrind-3.12.0.tar.bz2',
             sha256='67ca4395b2527247780f36148b084f5743a68ab0c850cb43e4a5b4b012cf76a1',
             when='@1.0.0:1.0.999')
    resource(name='valgrind-3.13.0',
             url='https://sourceware.org/pub/valgrind/valgrind-3.10.1.tar.bz2',
             sha256='fa253dc26ddb661b6269df58144eff607ea3f76a9bcfe574b0c7726e1dfcb997',
             when='@0.9.0:0.9.999')

    variant('fma', default=True,
            description='Activates fused multiply-add support for Verrou')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    def patch(self):
        # We start with the verrou source tree and a "valgrind-x.y.z" subdir.
        # But we actually need a valgrind source tree with a "verrou" subdir.
        # First, let's locate the valgrind sources...
        valgrind_dirs = glob.glob('valgrind-*')
        assert len(valgrind_dirs) == 1
        valgrind_dir = valgrind_dirs[0]

        # ...then we can flip the directory organization around
        verrou_files = os.listdir('.')
        verrou_files.remove(valgrind_dir)
        os.mkdir('verrou')
        for name in verrou_files:
            os.rename(name, os.path.join('verrou', name))
        for name in os.listdir(valgrind_dir):
            os.rename(os.path.join(valgrind_dir, name), name)
        os.rmdir(valgrind_dir)

        # Once this is done, we can patch valgrind
        which('patch')('-p0', '--input=verrou/valgrind.diff')

        # Autogenerated perl path may be too long, need to fix this here
        # because these files are used during the build.
        for link_tool_in in glob.glob('coregrind/link_tool_exe_*.in'):
            filter_file('^#! @PERL@',
                        '#! /usr/bin/env perl',
                        link_tool_in)

    def configure_args(self):
        spec = self.spec
        options = ['--enable-only64bit']

        options.append('--{}-verrou-fma'
                       .format('enable' if 'fma' in spec else 'disable'))

        if sys.platform == 'darwin':
            options.append('--build=amd64-darwin')

        return options
