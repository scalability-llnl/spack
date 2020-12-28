# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Mpi(Package):
    """Virtual package for the Message Passing Interface."""
    homepage = 'https://www.mpi-forum.org/'
    virtual = True

    def test(self):
        for lang in ('c', 'f'):
            filename = self.test_suite.current_test_data_dir.join(
                'mpi_hello.' + lang)

            compiler_var = 'MPICC' if lang == 'c' else 'MPIF90'
            compiler = os.environ[compiler_var]

            exe_name = 'mpi_hello_%s' % lang
            mpirun = join_path(self.prefix.bin, 'mpirun')

            compiled = self.run_test(compiler,
                                     options=['-o', exe_name, filename])
            if compiled:
                self.run_test(mpirun,
                              options=['-np', '1', exe_name],
                              expected=[r'Hello world! From rank \s*0 of \s*1']
                              )
