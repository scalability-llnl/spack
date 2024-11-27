# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStui(PythonPackage):
    """A Slurm dashboard for the terminal."""

    homepage = "https://github.com/mi-lad/stui"
    pypi = "stui/stui-0.3.6.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("0.3.6", sha256="b7f4f9ff537977af0d37a3218217f2b882a30709fcd2773a07df09050c700102")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-urwid", type=("build", "run"))
    depends_on("py-fabric@2.5.0:", type=("build", "run"))
