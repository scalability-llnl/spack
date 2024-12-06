# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJupytext(PythonPackage):
    """Jupyter Notebooks as Markdown Documents, Julia, Python or R scripts"""

    homepage = "https://github.com/mwouts/jupytext/"
    git = "https://github.com/mwouts/jupytext/"
    pypi = "jupytext/jupytext-1.13.0.tar.gz"

    maintainers("vvolkl")

    license("MIT")

    version("1.16.0", sha256="94c7e67775e90e1792c39ab7fca4e0459bf7c35656123e8dc2e9e1b3e953baf8")
    version("1.14.1", sha256="314fa0e732b1d14764271843b676938ef8a7b9d53c3575ade636b45d13f341c8")
    version("1.13.6", sha256="c6c25918ddb6403d0d8504e08d35f6efc447baf0dbeb6a28b73adf39e866a0c4")
    version("1.13.0", sha256="fb220af65d2bd32d01c779b0e935c4c2b71e3f5f2f01bf1bab10d5f23fe121d4")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.8:", type=("build", "run"), when="@1.16:")
    depends_on("python@3.6:3", type=("build", "run"), when="@:1.14")

    depends_on("py-hatchling@1.5.0:", type="build", when="@1.16:")
    depends_on("py-setuptools@40.8.0:", type="build", when="@:1.14.1")

    depends_on("py-nbformat", type=("build", "run"))
    depends_on("py-mdit-py-plugins", type=("build", "run"))
    depends_on("py-markdown-it-py@1.0:", type=("build", "run"), when="@1.16:")
    depends_on("py-markdown-it-py@1.0:2", type=("build", "run"), when="@1.14.1")
    depends_on("py-markdown-it-py@1.0:1", type=("build", "run"), when="@:1.13.6")
    depends_on("py-packaging", type=("build", "run"), when="@1.16:")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))

    # todo: in order to use jupytext as a jupyterlab extension,
    # some additional dependencies need to be added (and checked):
    depends_on("py-jupyterlab@4", type=("build", "run"), when="@1.16:")
    depends_on("py-jupyterlab@3", type=("build", "run"), when="@:1.14")
    depends_on("py-hatch-jupyter-builder@0.5:", type=("build", "run"), when="@1.16:")
    depends_on("py-jupyter-packaging@0.7.9:0.7", type="build", when="@:1.14")
