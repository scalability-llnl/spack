# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MultimethodBase(Package):
    """This is a base class for the Multimethod test case.

    It tests whether mutlimethod properly invokes methods in a base
    class when subclass multi-methods do not match.

    """

    homepage = "http://www.example.com/"
    url = "http://www.example.com/example-1.0.tar.gz"

    def base_method(self):
        return "base_method"

    def diamond_inheritance(self):
        return "base_package"
