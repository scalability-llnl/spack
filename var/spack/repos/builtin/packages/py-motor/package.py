# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMotor(PythonPackage):
    """async Python driver for MongoDB and Tornado or asyncio"""

    homepage = "https://github.com/mongodb/motor/"
    pypi = "motor/motor-2.5.1.tar.gz"

    license("Apache-2.0")

    version("2.5.1", sha256="663473f4498f955d35db7b6f25651cb165514c247136f368b84419cb7635f6b8")

    depends_on("python@3.5.2:", type=("build", "run"))
    depends_on("py-pymongo@3.12:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
