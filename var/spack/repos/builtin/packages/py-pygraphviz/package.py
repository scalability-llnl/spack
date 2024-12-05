# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygraphviz(PythonPackage):
    """Python interface to Graphviz"""

    homepage = "https://pygraphviz.github.io/"
    pypi = "pygraphviz/pygraphviz-1.7.zip"

    maintainers("haralmha")

    license("BSD-3-Clause")

    version("1.10", sha256="457e093a888128903251a266a8cc16b4ba93f3f6334b3ebfed92c7471a74d867")
    version("1.7", sha256="a7bec6609f37cf1e64898c59f075afd659106cf9356c5f387cecaa2e0cdb2304")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("python@3.8:", when="@1.10:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("graphviz")
