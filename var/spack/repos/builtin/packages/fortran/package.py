# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Fortran(Package):
    """Virtual package for the Fortran language."""

    homepage = "https://wg5-fortran.org/"
    virtual = True

    def test_fortran(self):
        """Compile and run 'Hello world'"""
        expected = ["Hello world", "YES!"]
        fc = which(os.environ["FC"])

        test_source = self.test_suite.current_test_data_dir
        for test in os.listdir(test_source):
            exe_name = f"{test}.exe"
            with test_part(self, f"test_fortran_{test}", f"run {exe_name}"):
                fc("-o", exe_name, join_path(test_source, test))
                exe = which(exe_name)
                out = exe(output=str.split, error=str.split)
                check_outputs(expected, out)
