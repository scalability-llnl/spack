# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMunkres(PythonPackage):
    """Python library for Munkres algorithm"""

    homepage = "https://github.com/bmc/munkres"
    pypi = "munkres/munkres-1.1.2.tar.gz"

    license("Apache-2.0")

    version("1.1.4", sha256="fc44bf3c3979dada4b6b633ddeeb8ffbe8388ee9409e4d4e8310c2da1792db03")
    version("1.1.2", sha256="81e9ced40c3d0ffc48be4b6da5cfdfaa49041faaaba8075b159974ec47926aea")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
