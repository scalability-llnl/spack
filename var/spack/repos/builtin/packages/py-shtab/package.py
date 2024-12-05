# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyShtab(PythonPackage):
    """Automatically generate shell tab completion scripts for python CLI apps."""

    homepage = "https://github.com/iterative/shtab"
    pypi = "shtab/shtab-1.3.3.tar.gz"

    license("Apache-2.0")

    version("1.3.4", sha256="353f2a3a5178cd2df8eb746e7ab26a5039a9989e4386de8fd239d8c1653a8887")
    version("1.3.3", sha256="1f7f263631acdf0a9e685bbf7126a0fa711c2d663db12441670b1cea3fa431d4")

    # setuptools and setuptools_scm imported in shtab/__init__.py
    depends_on("python@2.7:2.8,3.2:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")
