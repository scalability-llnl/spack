# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.mock.multimethod_base import MultimethodBase


class MultimethodDiamondParent(MultimethodBase):
    """This package is designed for use with Spack's multimethod test.
    It has a bunch of test cases for the @when decorator that the
    test uses.
    """

    @when("@3.0")
    def diamond_inheritance(self):
        return "second_parent"

    @when("@4.0, 2.0")
    def diamond_inheritance(self):
        return "should never be reached by diamond inheritance test"
