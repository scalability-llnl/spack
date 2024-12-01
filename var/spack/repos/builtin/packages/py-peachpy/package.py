# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPeachpy(PythonPackage):
    """Portable Efficient Assembly Codegen in Higher-level Python."""

    homepage = "https://github.com/Maratyszcza/PeachPy"
    git = "https://github.com/Maratyszcza/PeachPy.git"

    license("BSD-2-Clause")

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-opcodes@0.3.13:", type="build")
    depends_on("py-six", type=("build", "run"))
