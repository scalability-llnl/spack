# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetifaces(PythonPackage):
    """Portable network interface information"""

    homepage = (
        "https://0xbharath.github.io/python-network-programming/libraries/netifaces/index.html"
    )
    pypi = "netifaces/netifaces-0.10.5.tar.gz"

    license("Unlicense")

    version("0.10.5", sha256="59d8ad52dd3116fcb6635e175751b250dc783fb011adba539558bd764e5d628b")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
