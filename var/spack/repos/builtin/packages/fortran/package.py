# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Fortran(Package):
    """Virtual package for the Fortran language."""
    homepage = 'https://wg5-fortran.org/'
    virtual = True

    def test(self):
        test_source = self.test_suite.current_test_data_dir

        for test in os.listdir(test_source):
            filepath = os.path.join(test_source, test)
            exe_name = '%s.exe' % test

            fc_exe = os.environ['FC']
            fc_opts = ['-o', exe_name, filepath]

            compiled = self.run_test(fc_exe, options=fc_opts, installed=True)

            if compiled:
                expected = ['Hello world', 'YES!']
                self.run_test(exe_name, expected=expected)
