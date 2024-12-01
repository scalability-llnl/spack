# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonGet(PythonPackage):
    """Get values from JSON objects usings a path expression."""

    homepage = "https://github.com/srittau/python-json-get"
    url = "https://github.com/srittau/python-json-get/archive/v1.1.1.tar.gz"

    license("MIT")

    version("1.1.1", sha256="0d436f1f2dc8c51ab0249d964bb7f176d724131f76c14adf6fc4687e68ec37ab")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
