# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMpmath(PythonPackage):
    """A Python library for arbitrary-precision floating-point arithmetic."""

    homepage = "https://mpmath.org"
    pypi = "mpmath/mpmath-1.0.0.tar.gz"

    license("BSD-3-Clause")

    version("1.3.0", sha256="7a28eb2a9774d00c7bc92411c19a89209d5da7c4c9a9e227be8330a23a25b91f")
    version("1.2.1", sha256="79ffb45cf9f4b101a807595bcb3e72e0396202e0b1d25d689134b48c4216a81a")
    version("1.1.0", sha256="fc17abe05fbab3382b61a123c398508183406fa132e0223874578e20946499f6")
    version("1.0.0", sha256="04d14803b6875fe6d69e6dccea87d5ae5599802e4b1df7997bddd2024001050c")
    version("0.19", sha256="68ddf6426dcda445323467d89892d2cffbbd1ae0b31ac1241b1b671749d63222")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@36.7.0:", type="build", when="@1.2.0:")
    depends_on("py-setuptools-scm@1.7.0:", type="build", when="@1.2.0:1.2")
