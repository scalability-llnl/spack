# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxArgparse(PythonPackage):
    """Sphinx extension to automatically document argparse-based commands."""

    homepage = "https://pypi.org/project/sphinx-argparse"
    pypi = "sphinx-argparse/sphinx-argparse-0.3.1.tar.gz"

    maintainers("sethrj")

    license("MIT")

    version("0.3.1", sha256="82151cbd43ccec94a1530155f4ad34f251aaca6a0ffd5516d7fadf952d32dc1e")

    depends_on("python@2.7.0:2.7,3.5:", type=("build", "run"))
    depends_on("py-sphinx@1.2.0:", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
    depends_on("py-setuptools", type="build")
