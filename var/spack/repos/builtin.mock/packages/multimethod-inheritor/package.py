# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.mock.multimethod import Multimethod


class MultimethodInheritor(Multimethod):
    """This package is designed for use with Spack's multimethod test.
    It has a bunch of test cases for the @when decorator that the
    test uses.
    """

    @when("@1.0")
    def inherited_and_overridden(self):
        return "inheritor@1.0"

    #
    # Test multi-level inheritance
    #
    @when("@2:")
    def base_method(self):
        return "multimethod-inheritor"
