# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTyper(PythonPackage):
    """Typer, build great CLIs. Easy to code. Based on Python type hints."""

    homepage = "https://github.com/tiangolo/typer"
    pypi = "typer/typer-0.9.0.tar.gz"

    license("MIT")

    version("0.9.0", sha256="50922fd79aea2f4751a8e0408ff10d2662bd0c8bbfa84755a699f3bada2978b2")
    version("0.7.0", sha256="ff797846578a9f2a201b53442aedeb543319466870fbe1c701eab66dd7681165")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-flit-core@2.0:2", type="build")
    depends_on("py-click@7.1.1:8", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4.3:", type=("build", "run"), when="@0.9.0:")
