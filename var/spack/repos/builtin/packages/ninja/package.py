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


class Ninja(Package):
    """Ninja is a small build system with a focus on speed. It differs from
    other build systems in two major respects: it is designed to have its input
    files generated by a higher-level build system, and it is designed to run
    builds as fast as possible."""

    homepage = "https://ninja-build.org/"
    url      = "https://github.com/ninja-build/ninja/archive/v1.7.2.tar.gz"

    version('1.8.2', '5fdb04461cc7f5d02536b3bfc0300166')
    version('1.7.2', '7b482218757acbaeac4d4d54a3cd94e1')
    version('1.6.0', '254133059f2da79d8727f654d7198f43')

    depends_on('python', type=('build', 'run'))

    phases = ['configure', 'install']

    def configure(self, spec, prefix):
        python('configure.py', '--bootstrap')

    @run_after('configure')
    @on_package_attributes(run_tests=True)
    def test(self):
        ninja = Executable('./ninja')
        ninja('-j{0}'.format(make_jobs), 'ninja_test')
        ninja_test = Executable('./ninja_test')
        ninja_test()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('ninja', prefix.bin)
        install_tree('misc', prefix.misc)

        # Some distros like Fedora install a 'ninja-build' executable
        # instead of 'ninja'. Install both for uniformity.
        with working_dir(prefix.bin):
            symlink('ninja', 'ninja-build')
