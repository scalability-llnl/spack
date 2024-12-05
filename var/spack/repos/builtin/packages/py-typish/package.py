# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypish(PythonPackage):
    """Python library for type checking"""

    homepage = "https://github.com/ramonhagenaars/typish"
    url = "https://github.com/ramonhagenaars/typish/archive/v1.9.2.tar.gz"

    license("MIT")

    version("1.9.3", sha256="16f8ff022b7009a91529e363d0484465be57797b9cc34a193ca7e3c4c597e4bc")
    version("1.9.2", sha256="d0cd35aade6f974b2509771ac92aa1a5b4d9efe9c2c34127734539fd28e7145c")

    depends_on("py-setuptools", type="build")
