# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pipx(PythonPackage):
    """pipx is a tool to install and run Python applications in isolated environments"""

    homepage = "https://pypa.github.io/pipx/"
    pypi = "pipx/pipx-1.2.0.tar.gz"

    license("MIT")

    version("1.2.0", sha256="d1908041d24d525cafebeb177efb686133d719499cb55c54f596c95add579286")

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-hatchling@0.15.0:", type="build")

    depends_on("py-argcomplete@1.9.4:", type=("build", "run"))
    depends_on("py-colorama@0.4.4:", type=("build", "run"), when="platform=windows")
    depends_on("py-importlib-metadata@3.3.0:", type=("build", "run"), when="^python@3.7")
    depends_on("py-packaging@20.0:", type=("build", "run"))
    depends_on("py-userpath@1.6.0:", type=("build", "run"))
