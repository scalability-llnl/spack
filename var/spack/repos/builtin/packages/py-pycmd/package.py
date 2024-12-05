# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycmd(PythonPackage):
    """pycmd is a collection of command line tools for helping with Python
    development."""

    pypi = "pycmd/pycmd-1.2.tar.gz"

    license("MIT")

    version("1.2", sha256="adc1976c0106919e9338db20102b91009256dcfec924a66928d7297026f72477")

    depends_on("py-py@1.4.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
