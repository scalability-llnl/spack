# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrandalf(PythonPackage):
    """Grandalf is a Python package made for experimentations with graph
    drawing algorithms."""

    homepage = "https://github.com/bdcht/grandalf"
    url = "https://github.com/bdcht/grandalf/archive/v0.7.tar.gz"

    license("EPL-1.0")

    version("0.7", sha256="b3112299fe0a9123c088a16bf2f1b541d0d91199b77170a9739b569bd16a828e")
    version("0.6", sha256="928db4b90f7aff01e252a833951086b20d5958c00083411193c794de7bf59df2")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-pyparsing", type=("build", "run"))
    depends_on("py-pytest-runner", type="build")
    depends_on("py-setuptools", type="build")
