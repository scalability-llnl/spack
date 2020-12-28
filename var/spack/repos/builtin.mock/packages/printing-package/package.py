# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PrintingPackage(Package):
    """This package prints some output from its install method.

    We use this to test whether that output is properly logged.
    """
    homepage = "http://www.example.com/printing_package"
    url      = "http://www.unit-test-should-replace-this-url/trivial_install-1.0.tar.gz"

    version('1.0', 'foobarbaz')

    def install(self, spec, prefix):
        print("BEFORE INSTALL")

        configure('--prefix=%s' % prefix)
        make()
        make('install')

        print("AFTER INSTALL")

    def test(self):
        print("BEFORE TEST")
        self.run_test('true')  # run /bin/true
        print("AFTER TEST")
