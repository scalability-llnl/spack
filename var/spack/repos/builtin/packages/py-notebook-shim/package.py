# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNotebookShim(PythonPackage):
    """A shim layer for notebook traits and config."""

    homepage = "https://github.com/jupyter/notebook_shim"
    pypi = "notebook_shim/notebook_shim-0.2.2.tar.gz"

    version("0.2.2", sha256="090e0baf9a5582ff59b607af523ca2db68ff216da0c69956b62cab2ef4fc9c3f")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-hatchling@1:", type="build")

    depends_on("py-jupyter-server@1.8:2", type=("build", "run"))
