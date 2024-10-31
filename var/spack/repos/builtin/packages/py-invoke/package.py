# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInvoke(PythonPackage):
    """Pythonic task execution"""

    homepage = "https://www.pyinvoke.org/"
    pypi = "invoke/invoke-1.4.1.tar.gz"

    license("BSD-2-Clause")

    version("2.2.0", sha256="ee6cbb101af1a859c7fe84f2a264c059020b0cb7fe3535f9424300ab568f6bd5")
    version("1.4.1", sha256="de3f23bfe669e3db1085789fd859eb8ca8e0c5d9c20811e2407fa042e8a5e15d")
    version("1.2.0", sha256="dc492f8f17a0746e92081aec3f86ae0b4750bf41607ea2ad87e5a7b5705121b7")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@2:")
    depends_on("py-setuptools", type="build")
