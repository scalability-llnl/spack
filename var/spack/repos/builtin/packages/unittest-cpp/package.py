# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UnittestCpp(CMakePackage):
    """UnitTest++ is a lightweight unit testing framework for C++. It was
    designed to do test-driven development on a wide variety of platforms.
    Simplicity, portability, speed, and small footprint are all very
    important aspects of UnitTest++. UnitTest++ is mostly standard C++ and
    makes minimal use of advanced library and language features, which
    means it should be easily portable to just about any platform."""

    homepage = "https://github.com/unittest-cpp/unittest-cpp/wiki"
    url = "https://github.com/unittest-cpp/unittest-cpp/archive/v1.6.0.tar.gz"

    license("MIT")

    version("2.0.0", sha256="74852198877dc2fdebdc4e5e9bd074018bf8ee03a13de139bfe41f4585b2f5b9")
    version("1.6.0", sha256="9fa7e797816e16669d68171418b0dc41ec6b7eaf8483f782441f5f159598c3c0")

    depends_on("cxx", type="build")  # generated
