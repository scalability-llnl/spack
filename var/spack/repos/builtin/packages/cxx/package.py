# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Cxx(Package):
    """Virtual package for the C++ language."""
    homepage = 'https://isocpp.org/std/the-standard'
    virtual = True

    def test(self):
        test_source = self.test_suite.current_test_data_dir

        for test in os.listdir(test_source):
            filepath = os.path.join(test_source, test)
            exe_name = '%s.exe' % test

            cxx_exe = os.environ['CXX']

            # standard options
            # Hack to get compiler attributes
            # TODO: remove this when compilers are dependencies
            c_name = clang if self.spec.satisfies('llvm+clang') else self.name
            c_spec = spack.spec.CompilerSpec(c_name, self.spec.version)
            c_cls = spack.compilers.class_for_compiler_name(c_name)
            compiler = c_cls(c_spec, None, None, ['fakecc', 'fakecxx'])

            cxx_opts = [compiler.cxx11_flag] if 'c++11' in test else []

            cxx_opts += ['-o', exe_name, filepath]
            compiled = self.run_test(cxx_exe, options=cxx_opts, installed=True)

            if compiled:
                expected = ['Hello world', 'YES!']
                self.run_test(exe_name, expected=expected)
