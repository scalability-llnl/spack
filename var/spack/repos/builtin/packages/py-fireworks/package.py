# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFireworks(PythonPackage):
    """FireWorks stores, executes, and manages calculation workflows."""

    homepage = "https://github.com/materialsproject/fireworks"
    pypi = "FireWorks/FireWorks-2.0.3.tar.gz"

    maintainers("meyersbs")

    version("2.0.3", sha256="5ba8f5dbd3867a34fc2c7836db0698ec4bbdf9c3ade58cf40a721a2f090c13f8")

    # From setup.py:
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-ruamel-yaml@0.15.35:", type=("build", "run"))
    depends_on("py-pymongo@3.3.0:", type=("build", "run"))
    depends_on("py-jinja2@2.8.0:", type=("build", "run"))
    depends_on("py-six@1.10.0:", type=("build", "run"))
    depends_on("py-monty@1.0.1:", type=("build", "run"))
    depends_on("py-python-dateutil@2.5.3:", type=("build", "run"))
    depends_on("py-tabulate@0.7.5:", type=("build", "run"))
    depends_on("py-flask@0.11.1:", type=("build", "run"))
    depends_on("py-flask-paginate@0.4.5:", type=("build", "run"))
    depends_on("py-gunicorn@19.6.0:", type=("build", "run"))
    depends_on("py-tqdm@4.8.4:", type=("build", "run"))
    depends_on("py-importlib-metadata@4.8.2:", when="^python@:3.7", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
