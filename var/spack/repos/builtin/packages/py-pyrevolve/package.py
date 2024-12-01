# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyrevolve(PythonPackage):
    """PyRevolve.

    Python wrapper for Revolve: https://dl.acm.org/doi/10.1145/347837.347846
    """

    homepage = "https://github.com/devitocodes/pyrevolve"
    pypi = "pyrevolve/pyrevolve-2.2.tar.gz"

    license("MIT")

    version("2.2", sha256="b49aea5cd6c520ac5fcd1d25fa23fe2c5502741d2965f3eee10be067e7b0efb4")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-contexttimer", type=("build", "run"))
    depends_on("py-cython@0.17:", type="build")
    depends_on("py-versioneer", type="build")
