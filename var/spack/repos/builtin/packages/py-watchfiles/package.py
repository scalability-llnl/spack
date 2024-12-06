# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWatchfiles(PythonPackage):
    """Simple, modern and high performance file watching and code reload in python."""

    homepage = "https://github.com/samuelcolvin/watchfiles"
    pypi = "watchfiles/watchfiles-0.18.1.tar.gz"

    license("MIT")

    version("0.18.1", sha256="4ec0134a5e31797eb3c6c624dbe9354f2a8ee9c720e0b46fc5b7bab472b7c6d4")

    depends_on("py-maturin@0.13", type="build")
    depends_on("py-anyio@3:", type=("build", "run"))
