# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatch(PythonPackage):
    """Modern, extensible Python project management"""

    homepage = "https://hatch.pypa.io/latest/"
    pypi = "hatch/hatch-1.12.0.tar.gz"

    license("MIT")

    version("1.12.0", sha256="ae80478d10312df2b44d659c93bc2ed4d33aecddce4b76378231bdf81c8bf6ad")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-hatchling@1.24.2:", type="build")
    depends_on("py-hatch-vcs@0.3.0:", type="build")
    depends_on("py-pyproject-hooks", type=("build"))

    depends_on("py-click@8.0.6:", type=("build", "run"))
    depends_on("py-httpx@0.22.0:", type=("build", "run"))
    depends_on("py-hyperlink@21.0.0:", type=("build", "run"))
    depends_on("py-keyring@23.5.0:", type=("build", "run"))
    depends_on("py-packaging@23.2:", type=("build", "run"))
    depends_on("py-pexpect@4.8:4.8", type=("build", "run"))
    depends_on("py-platformdirs@2.5.0:", type=("build", "run"))
    depends_on("py-rich@11.2.0:", type=("build", "run"))
    depends_on("py-shellingham@1.4.0:", type=("build", "run"))
    depends_on("py-tomli-w@1.0:", type=("build", "run"))
    depends_on("py-tomlkit@0.11.1:", type=("build", "run"))
    depends_on("py-userpath@1.7:1.7", type=("build", "run"))
    depends_on("py-uv@0.1.35:", type=("build", "run"))
    depends_on("py-virtualenv@20.26.1:", type=("build", "run"))
    depends_on("py-zstandard@:1", type=("build", "run"))
