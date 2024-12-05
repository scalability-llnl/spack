# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUnidecode(PythonPackage):
    """ASCII transliterations of Unicode text"""

    pypi = "unidecode/Unidecode-1.1.1.tar.gz"

    license("GPL-2.0-or-later")

    version("1.1.1", sha256="2b6aab710c2a1647e928e36d69c21e76b453cd455f4e2621000e54b2a9b8cce8")
    version("0.04.21", sha256="280a6ab88e1f2eb5af79edff450021a0d3f0448952847cd79677e55e58bad051")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
