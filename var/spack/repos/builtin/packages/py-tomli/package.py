# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTomli(PythonPackage):
    """Tomli is a Python library for parsing TOML.

    Tomli is fully compatible with TOML v1.0.0."""

    homepage = "https://github.com/hukkin/tomli"
    pypi = "tomli/tomli-2.0.1.tar.gz"
    git = "https://github.com/hukkin/tomli.git"

    maintainers("charmoniumq")

    license("MIT")

    version("2.0.1", sha256="de526c12914f0c550d15924c62d72abc48d6fe7364aa87328337a31007fe8a4f")
    version("1.2.2", sha256="c6ce0015eb38820eaf32b5db832dbc26deb3dd427bd5f6556cf0acac2c214fee")
    version("1.2.1", sha256="a5b75cb6f3968abb47af1b40c1819dc519ea82bcc065776a866e8d74c5ca9442")

    # https://github.com/hukkin/tomli/blob/2.0.1/pyproject.toml#L2
    depends_on("py-flit-core@3.2:3", type="build")

    # https://github.com/hukkin/tomli/blob/2.0.1/pyproject.toml#L13
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"), when="@2.0.1:")
