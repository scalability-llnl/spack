# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------
from spack.package import *


class PyRequirementsParser(PythonPackage):
    """This is a small Python module for parsing Pip requirement files.
    The goal is to parse everything in the Pip requirement file format spec."""

    homepage = "https://github.com/madpah/requirements-parser"
    pypi = "requirements-parser/requirements-parser-0.5.0.tar.gz"

    maintainers("DaxLynch", "eugeneswalker")

    license("Apache-2.0")

    version("0.5.0", sha256="3336f3a3ae23e06d3f0f88595e4052396e3adf91688787f637e5d2ca1a904069")

    depends_on("python@3.6:3.99", type=("build", "run"))

    depends_on("py-poetry-core@1:", type="build")

    depends_on("py-types-setuptools@57:", type=("build", "run"))
