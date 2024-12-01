# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFilecheck(PythonPackage):
    """Python port of LLVM's FileCheck, flexible pattern matching file verifier."""

    pypi = "filecheck/filecheck-0.0.23.tar.gz"

    license("Apache-2.0")

    version("0.0.23", sha256="1c5db511fb7b5a32e1e24736479cfe754ea27c9ae0d5b6d52c0af132c8db3e7d")

    depends_on("python@3.6.2:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
