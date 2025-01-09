# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDnspython(PythonPackage):
    """DNS toolkit"""

    homepage = "https://www.dnspython.org"
    pypi = "dnspython/dnspython-2.2.1.tar.gz"

    license("ISC")

    version("2.6.1", sha256="e8f0f9c23a7b7cb99ded64e6c3a6f3e701d78f50c55e002b839dea7225cff7cc")
    version("2.2.1", sha256="0f7569a4a6ff151958b64304071d370daa3243d15941a7beedf0c9fe5105603e")

    depends_on("python@3.8:", type=("build", "run"), when="@2.5:")
    depends_on("python@3.7:", type=("build", "run"), when="@2.4:")
    depends_on("python@3.6:3", type=("build", "run"), when="@:2.3")
    depends_on("py-poetry-core", type="build", when="@:2.3")
    depends_on("py-hatchling@1.17:", type="build", when="@2.4:")
    depends_on("py-hatchling@1.21:", type="build", when="@2.6:")
