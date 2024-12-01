# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterPackaging(PythonPackage):
    """Jupyter Packaging Utilities."""

    homepage = "https://github.com/jupyter/jupyter-packaging"
    pypi = "jupyter_packaging/jupyter_packaging-0.10.4.tar.gz"

    tags = ["build-tools"]

    license("BSD-3-Clause")

    version("0.12.3", sha256="9d9b2b63b97ffd67a8bc5391c32a421bc415b264a32c99e4d8d8dd31daae9cf4")
    version("0.12.0", sha256="b27455d60adc93a7baa2e0b8f386be81b932bb4e3c0116046df9ed230cd3faac")
    version("0.11.1", sha256="6f5c7eeea98f7f3c8fb41d565a94bf59791768a93f93148b3c2dfb7ebade8eec")
    version("0.10.6", sha256="a8a2c90bf2e0cae83be63ccb0b7035032a1589f268cc08b1d479e37ce50fc940")
    version("0.10.4", sha256="589db027cb85a92612f9bcfaeecaa8a9072ac8a4bddaf827f648664258e587c4")
    version(
        "0.7.12",
        sha256="b140325771881a7df7b7f2d14997b619063fe75ae756b9025852e4346000bbb8",
        # name has a '-' instead of a '_'
        url="https://files.pythonhosted.org/packages/source/j/jupyter_packaging/jupyter-packaging-0.7.12.tar.gz",
    )

    # https://github.com/jupyter/jupyter-packaging/pull/153
    depends_on("python@:3.12", when="@:0.12.1", type=("build", "run"))
    depends_on("py-hatchling@0.25:", when="@0.12.1:", type="build")
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-tomlkit", when="@0.8:", type=("build", "run"))
    depends_on("py-setuptools@60.2:", when="@0.12:", type=("build", "run"))
    depends_on("py-setuptools@46.4:", when="@0.8:", type=("build", "run"))
    # https://github.com/jupyter/jupyter-packaging/issues/130
    depends_on("py-setuptools@:60", when="@:0.11", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-wheel", when="@0.8:", type=("build", "run"))
    depends_on("py-deprecation", when="@0.8:", type=("build", "run"))
