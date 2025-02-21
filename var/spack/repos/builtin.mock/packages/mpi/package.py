# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpi(Package):
    """Virtual package for the Message Passing Interface."""

    homepage = "https://www.mpi-forum.org/"
    virtual = True

    def test_hello(self):
        print("Hello there!")
