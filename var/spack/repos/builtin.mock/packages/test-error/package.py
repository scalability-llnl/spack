# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TestError(Package):
    """This package has a test method that fails in a subprocess."""

    homepage = "http://www.example.com/test-failure"
    url      = "http://www.test-failure.test/test-failure-1.0.tar.gz"

    version('1.0', 'foobarbaz')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

    def test(self):
        self.run_test('false')
