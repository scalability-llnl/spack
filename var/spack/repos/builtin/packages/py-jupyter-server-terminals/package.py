# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterServerTerminals(PythonPackage):
    """A Jupyter Server Extension Providing Terminals."""

    homepage = "https://github.com/jupyter-server/jupyter_server_terminals"
    pypi = "jupyter_server_terminals/jupyter_server_terminals-0.4.4.tar.gz"

    version("0.4.4", sha256="57ab779797c25a7ba68e97bcfb5d7740f2b5e8a83b5e8102b10438041a7eac5d")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-hatchling@1.5:", type="build")

    # for windows depends_on pywinpty@2.0.3:
    # py-pywinpty is not in spack and requires the build system maturin
    depends_on("py-terminado@0.8.3:", type=("build", "run"))

    # to prevent: ModuleNotFoundError: Jupyter Server must be installed to use this extension.
    # there should be a dependency on `py-jupyter-server` but this would create
    # a cyclic dependency
    skip_modules = ["jupyter_server_terminals"]
