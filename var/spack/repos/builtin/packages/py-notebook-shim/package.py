# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNotebookShim(PythonPackage):
    """A shim layer for notebook traits and config."""

    homepage = "https://github.com/jupyter/notebook_shim"
    pypi = "notebook_shim/notebook_shim-0.2.2.tar.gz"

    license("BSD-3-Clause")

    version("0.2.3", sha256="f69388ac283ae008cd506dda10d0288b09a017d822d5e8c7129a152cbd3ce7e9")
    version("0.2.2", sha256="090e0baf9a5582ff59b607af523ca2db68ff216da0c69956b62cab2ef4fc9c3f")

    depends_on("py-hatchling@1:", type="build")

    depends_on("py-jupyter-server@1.8:2", type=("build", "run"))
