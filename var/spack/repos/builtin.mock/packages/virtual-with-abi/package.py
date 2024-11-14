# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class VirtualWithAbi(Package):
    """Virtual package for mocking an interface with stable ABI ."""

    homepage = "https://www.abi.org/"
    virtual = True

    def test_hello(self):
        print("Hello there!")
