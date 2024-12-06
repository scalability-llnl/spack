# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class WithConstraintMet(Package):
    """Package that tests True when specs on directives."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/example-1.0.tar.gz"

    version("2.0", md5="0123456789abcdef0123456789abcdef")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    with when("@1.0"):
        depends_on("pkg-b")
        conflicts("%gcc", when="+foo")

    with when("@0.14: ^pkg-b@:4.0"):
        depends_on("pkg-c", when="@:15 ^pkg-b@3.8:")
