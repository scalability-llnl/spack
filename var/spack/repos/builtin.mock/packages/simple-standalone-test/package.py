# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SimpleStandaloneTest(Package):
    """This package has simple stand-alone test features."""

    homepage = "http://www.example.com/simple_test"
    url = "http://www.unit-test-should-replace-this-url/simple_test-1.0.tar.gz"

    version("1.0", md5="123456789abcdef0123456789abcdefg")
    version("0.9", md5="0123456789abcdef0123456789abcdef")

    provides("standalone-ifc")

    def test_echo(self):
        """simple stand-alone test"""
        echo = which("echo")
        echo("testing echo", output=str.split, error=str.split)

    def test_skip(self):
        """simple skip test"""
        if self.spec.satisfies("@1.0:"):
            raise SkipTest("This test is not available from v1.0 on")

        print("Ran test_skip")
