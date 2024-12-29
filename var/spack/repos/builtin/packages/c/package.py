# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class C(Package):
    """Virtual package for C compilers."""

    homepage = "http://open-std.org/JTC1/SC22/WG14/www/standards"
    virtual = True

    def test_c(self):
        """build and run C examples"""
        cc = which(os.environ["CC"])
        expected = ["Hello world", "YES!"]

        test_source = self.test_suite.current_test_data_dir
        for test in os.listdir(test_source):
            exe_name = f"{test}.exe"
            with test_part(self, f"test_c_{test}", f"build and run {exe_name}"):
                filepath = join_path(test_source, test)
                cc("-o", exe_name, filepath)
                exe = which(exe_name)
                out = exe(output=str.split, error=str.split)
                check_outputs(expected, out)
