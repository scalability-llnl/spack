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

    def test_hello_world(self):
        """Compile and run 'Hello world'"""
        test_source = self.test_suite.current_test_data_dir

        for test in os.listdir(test_source):
            with test_part(self, f"test_hello_world_{test}", f"Test {test}"):
                filepath = os.path.join(test_source, test)
                exe_name = "%s.exe" % test
                fc_exe = os.environ["FC"]
                fc_opts = ["-o", exe_name, filepath]
                compiled = self.run_test(fc_exe, options=fc_opts, installed=True)

                if compiled:
                    exe = which(join_path(self.prefix.bin, exe_name))
                    if exe is None:
                        raise SkipTest(f"{exe} not found in {self.version}")
                        expected = ["Hello world", "YES!"]
                        out = exe(output=str.split, error=str.split)
                        check_outputs(expected, out)
                    else:
                        assert False, "Did not compile"
