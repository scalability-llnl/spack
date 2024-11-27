# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeotime(PythonPackage):
    """Nanosecond resolution temporal types"""

    homepage = "https://github.com/neo4j-drivers/neotime"
    pypi = "neotime/neotime-1.7.4.tar.gz"

    license("Apache-2.0")

    version("1.7.4", sha256="4e0477ba0f24e004de2fa79a3236de2bd941f20de0b5db8d976c52a86d7363eb")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytz", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
