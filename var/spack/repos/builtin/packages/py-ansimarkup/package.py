# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnsimarkup(PythonPackage):
    """Produce colored terminal text with an xml-like markup."""

    homepage = "https://github.com/gvalkov/python-ansimarkup"
    pypi = "ansimarkup/ansimarkup-1.5.0.tar.gz"

    maintainers("LydDeb")

    license("BSD-3-Clause")

    version("2.1.0", sha256="7b3e3d93fecc5b64d23a6e8eb96dbc8b0b576a211829d948afb397d241a8c51b")
    version("1.5.0", sha256="96c65d75bbed07d3dcbda8dbede8c2252c984f90d0ca07434b88a6bbf345fad3")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@61:", type="build", when="@2.1.0")
    depends_on("py-colorama", type=("build", "run"))
