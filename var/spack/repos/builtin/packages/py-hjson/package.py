# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyHjson(PythonPackage):
    """Hjson is an user interface for JSON.
    The Python implementation of Hjson is based on simplejson."""

    homepage = "https://github.com/hjson/hjson-py"
    pypi = "hjson/hjson-3.0.2.tar.gz"

    license("AFL-2.1")

    version("3.1.0", sha256="55af475a27cf83a7969c808399d7bccdec8fb836a07ddbd574587593b9cdcf75")
    version("3.0.2", sha256="2838fd7200e5839ea4516ece953f3a19892c41089f0d933ba3f68e596aacfcd5")

    depends_on("py-setuptools", type="build")
