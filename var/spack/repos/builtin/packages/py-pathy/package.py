# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPathy(PythonPackage):
    """pathlib.Path subclasses for local and cloud bucket storage"""

    homepage = "https://github.com/justindujardin/pathy"
    pypi = "pathy/pathy-0.10.1.tar.gz"

    license("Apache-2.0")

    version("0.10.1", sha256="4cd6e71b4cd5ff875cfbb949ad9fa5519d8d1dbe69d5fc1d1b23aa3cb049618b")

    depends_on("py-setuptools", type="build")
    depends_on("py-smart-open@5.2.1:6", type=("build", "run"))
    depends_on("py-typer@0.3:0", type=("build", "run"))
