# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PrintingPackage(Package):
    """This package prints some output from its install method.

    We use this to test whether that output is properly logged.
    """

    homepage = "http://www.example.com/printing_package"
    url = "http://www.unit-test-should-replace-this-url/trivial_install-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        print("BEFORE INSTALL")

        mkdirp(prefix)
        touch(os.path.join(prefix, "dummyfile"))

        print("AFTER INSTALL")

    def test_print(self):
        """Test print example."""

        print("Running test_print")
        print("And a second command")
