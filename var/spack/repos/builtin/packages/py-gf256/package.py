# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGf256(PythonPackage):
    """GF256 is an implementation of GF(2**8). This Galois Field allows you
    to perform finite field arithmetic on byte sized integers."""

    homepage = "https://github.com/DasIch/gf256/"
    url = "https://github.com/DasIch/gf256/archive/0.2.0.tar.gz"

    version("0.2.0", sha256="75966f57674d957fba361b4d41a19ea0989dd55532ca7df1797b1d5c5a67ad71")

    depends_on("py-setuptools", type="build")
    depends_on("py-cffi@1.7.0:", type=("build", "run"))
