# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


def check(condition, msg):
    """Raise an install error if condition is False."""
    if not condition:
        raise InstallError(msg)


class CmakeClientDep(CMakePackage):
    """A dummy package that uses cmake."""

    homepage = "https://www.example.com"
    url = "https://www.example.com/cmake-client-1.0.tar.gz"

    version("1.0", sha256="a5b529fb5415a8a33281ddde4317bd68bd6a2317db1f96565c541c53f67e8f9a")

    depends_on("cmake-client")
