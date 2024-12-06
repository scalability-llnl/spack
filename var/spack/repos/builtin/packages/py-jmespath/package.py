# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJmespath(PythonPackage):
    """JSON Matching Expressions."""

    homepage = "https://github.com/jmespath/jmespath.py"
    pypi = "jmespath/jmespath-0.9.4.tar.gz"

    license("MIT")

    version("1.0.1", sha256="90261b206d6defd58fdd5e85f478bf633a2901798906be2ad389150c5c60edbe")
    version("0.10.0", sha256="b85d0567b8666149a93172712e68920734333c0ce7e89b78b3e987f71e5ed4f9")
    version("0.9.4", sha256="bde2aef6f44302dfb30320115b17d030798de8c4110e28d5cf6cf91a7a31074c")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.7:", type=("build", "run"), when="@1.0.0:")
