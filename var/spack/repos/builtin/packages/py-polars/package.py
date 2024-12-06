# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPolars(PythonPackage):
    """Blazingly fast DataFrame library."""

    homepage = "https://www.pola.rs/"
    pypi = "polars/polars-0.20.5.tar.gz"

    license("MIT")

    version("0.20.5", sha256="fa4abc22cee024b5872961ddcd8a13a0a76150df345e21ce4308c2b1a36b47aa")

    # pyproject.toml
    depends_on("py-maturin@1.3.2:", type="build")

    # README.md
    depends_on("rust@1.71:", type="build")
