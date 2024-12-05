# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribProgramoutput(PythonPackage):
    """A Sphinx extension to literally insert the output of arbitrary commands
    into documents, helping you to keep your command examples up to date."""

    homepage = "https://sphinxcontrib-programoutput.readthedocs.org/"
    pypi = "sphinxcontrib-programoutput/sphinxcontrib-programoutput-0.15.tar.gz"

    license("BSD-2-Clause")

    version("0.15", sha256="80dd5b4eab780a13ff2c23500cac3dbf0e04ef9976b409ef25a47c263ef8ab94")
    version("0.10", sha256="fdee94fcebb0d8fddfccac5c4fa560f6177d5340c4349ee447c890bea8857094")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx@1.7.0:", type=("build", "run"))
