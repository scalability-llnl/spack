# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPuremagic(PythonPackage):
    """puremagic is a pure python module that will identify a file based off its magic numbers."""

    homepage = "https://github.com/cdgriffith/puremagic"
    pypi = "puremagic/puremagic-1.10.tar.gz"

    license("MIT")

    version("1.14", sha256="3d5df26cc7ec9aebbf842a09115a2fa85dc59ea6414fa568572c44775d796cbc")
    version("1.10", sha256="6ffea02b80ceec1381f9df513e0120b701a74b6efad92311ea80281c7081b108")

    depends_on("py-setuptools", type="build")
