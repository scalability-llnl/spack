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
import os
import shutil
from tempfile import mkdtemp

from llnl.util.filesystem import set_executable, mkdirp

import spack.spec
import spack.cmd.compiler
import spack.compilers
from spack.version import Version
from spack.test.mock.packages_test import *

test_version = '4.5-spacktest'


class MockArgs(object):

    def __init__(self, add_paths=[], scope=None, compiler_spec=None, all=None):
        self.add_paths = add_paths
        self.scope = scope
        self.compiler_spec = compiler_spec
        self.all = all


def make_mock_compiler():
    """Make a directory containing a fake, but detectable compiler."""
    mock_compiler_dir = mkdtemp()
    bin_dir = os.path.join(mock_compiler_dir, 'bin')
    mkdirp(bin_dir)

    gcc_path = os.path.join(bin_dir, 'gcc')
    gxx_path = os.path.join(bin_dir, 'g++')
    gfortran_path = os.path.join(bin_dir, 'gfortran')

    with open(gcc_path, 'w') as f:
        f.write("""\
#!/bin/sh

for arg in "$@"; do
    if [ "$arg" = -dumpversion ]; then
        echo '%s'
    fi
done
""" % test_version)

    # Create some mock compilers in the temporary directory
    set_executable(gcc_path)
    shutil.copy(gcc_path, gxx_path)
    shutil.copy(gcc_path, gfortran_path)

    return mock_compiler_dir


class CompilerCmdTest(MockPackagesTest):
    """ Test compiler commands for add and remove """

    def test_compiler_remove(self):
        args = MockArgs(all=True, compiler_spec='gcc@4.5.0')
        spack.cmd.compiler.compiler_remove(args)
        compilers = spack.compilers.all_compilers()
        self.assertTrue(spack.spec.CompilerSpec("gcc@4.5.0") not in compilers)

    def test_compiler_add(self):
        # compilers available by default.
        old_compilers = set(spack.compilers.all_compilers())

        # add our new compiler and find again.
        compiler_dir = make_mock_compiler()

        try:
            args = MockArgs(add_paths=[compiler_dir])
            spack.cmd.compiler.compiler_find(args)

            # ensure new compiler is in there
            new_compilers = set(spack.compilers.all_compilers())
            new_compiler = new_compilers - old_compilers
            self.assertTrue(new_compiler)
            self.assertTrue(new_compiler.pop().version ==
                            Version(test_version))

        finally:
            shutil.rmtree(compiler_dir, ignore_errors=True)
