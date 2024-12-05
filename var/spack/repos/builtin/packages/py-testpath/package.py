# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTestpath(PythonPackage):
    """Testpath is a collection of utilities for Python code working with
    files and commands."""

    homepage = "https://github.com/jupyter/testpath"
    pypi = "testpath/testpath-0.4.2.tar.gz"

    license("BSD-3-Clause")

    version("0.6.0", sha256="2f1b97e6442c02681ebe01bd84f531028a7caea1af3825000f52345c30285e0f")
    version("0.5.0", sha256="1acf7a0bcd3004ae8357409fc33751e16d37ccc650921da1094a86581ad1e417")
    version("0.4.2", sha256="b694b3d9288dbd81685c5d2e7140b81365d46c29f5db4bc659de5aa6b98780f8")

    depends_on("python@3.5:", type=("build", "run"), when="@0.5.0:")
    depends_on("py-flit-core@3.2.0:3.2", type="build", when="@:0.5.0")
    depends_on("py-flit-core@3.2.0:3", type="build", when="@0.6.0:")
