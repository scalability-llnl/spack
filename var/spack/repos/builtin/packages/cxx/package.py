# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Cxx(Package):
    """Virtual package for the C++ language."""

    homepage = "https://isocpp.org/std/the-standard"
    virtual = True

    def test_cxx(self):
        """Compile and run 'Hello World'"""
        cxx = which(os.environ["CXX"])
        expected = ["Hello world", "YES!"]

        test_source = self.test_suite.current_test_data_dir
        for test in os.listdir(test_source):
            exe_name = f"{test}.exe"
            filepath = test_source.join(test)
            with test_part(self, f"test_cxx_{test}", f"build and run {exe_name}"):
                # standard options
                # Hack to get compiler attributes
                # TODO: remove this when compilers are dependencies
                c_name = clang if self.spec.satisfies("llvm+clang") else self.name
                c_spec = spack.spec.CompilerSpec(c_name, self.spec.version)
                c_cls = spack.compilers.class_for_compiler_name(c_name)
                compiler = c_cls(c_spec, None, None, ["fakecc", "fakecxx"])
                cxx_opts = [compiler.cxx11_flag] if "c++11" in test else []
                cxx_opts += ["-o", exe_name, filepath]

                cxx(*cxx_opts)
                exe = which(exe_name)
                out = exe(output=str.split, error=str.split)
                check_outputs(expected, out)
