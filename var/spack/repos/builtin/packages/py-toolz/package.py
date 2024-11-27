# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyToolz(PythonPackage):
    """A set of utility functions for iterators, functions, and dictionaries"""

    homepage = "https://github.com/pytoolz/toolz/"
    pypi = "toolz/toolz-0.9.0.tar.gz"

    license("BSD-3-Clause")

    version("0.12.0", sha256="88c570861c440ee3f2f6037c4654613228ff40c93a6c25e0eba70d17282c6194")
    version("0.9.0", sha256="929f0a7ea7f61c178bd951bdae93920515d3fbdbafc8e6caf82d752b9b3b31c9")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.5:", type=("build", "run"), when="@0.11.0:")
