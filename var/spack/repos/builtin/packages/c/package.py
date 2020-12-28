# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class C(Package):
    """Virtual package for C compilers."""
    homepage = 'http://open-std.org/JTC1/SC22/WG14/www/standards'
    virtual = True

    def test(self):
        test_source = self.test_suite.current_test_data_dir

        for test in os.listdir(test_source):
            filepath = test_source.join(test)
            exe_name = '%s.exe' % test

            cc_exe = os.environ['CC']
            cc_opts = ['-o', exe_name, filepath]
            compiled = self.run_test(cc_exe, options=cc_opts, installed=True)

            if compiled:
                expected = ['Hello world', 'YES!']
                self.run_test(exe_name, expected=expected)
