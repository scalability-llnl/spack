# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpretty(PythonPackage):
    """HTTP client mock for Python."""

    homepage = "https://httpretty.readthedocs.io/en/latest/"
    pypi = "httpretty/httpretty-1.1.3.tar.gz"

    license("MIT")

    version("1.1.4", sha256="20de0e5dd5a18292d36d928cc3d6e52f8b2ac73daec40d41eb62dee154933b68")
    version("1.1.3", sha256="229ade39175ea4324e767f29dc24e5f846fbc72bf80e1a919b2547a6574ff601")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
