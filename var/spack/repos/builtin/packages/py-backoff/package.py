# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackoff(PythonPackage):
    """Function decoration for backoff and retry."""

    homepage = "https://github.com/litl/backoff"
    pypi = "backoff/backoff-2.2.1.tar.gz"

    license("MIT")

    version("2.2.1", sha256="03f829f5bb1923180821643f8753b0502c3b682293992485b0eef2807afa5cba")

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
