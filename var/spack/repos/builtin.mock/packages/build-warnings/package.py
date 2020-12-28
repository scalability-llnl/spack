# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BuildWarnings(Package):
    """This package's install fails but only emits warnings."""

    homepage = "http://www.example.com/trivial_install"
    url      = "http://www.unit-test-should-replace-this-url/trivial_install-1.0.tar.gz"

    version('1.0', 'foobarbaz')

    def install(self, spec, prefix):
        with open('configure', 'w') as f:
            f.write("""#!/bin/sh\n
echo 'checking for gcc... /Users/gamblin2/src/spack/lib/spack/env/clang/clang'
echo 'checking whether the C compiler works... yes'
echo 'checking for C compiler default output file name... a.out'
echo 'WARNING: ALL CAPITAL WARNING!'
echo 'checking for suffix of executables...'
echo 'foo.c:89: warning: some weird warning!'
exit 1
""")
        configure()
