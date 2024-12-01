# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReportseff(PythonPackage):
    """A python script for tabular display of slurm efficiency information."""

    homepage = "https://github.com/troycomi/reportseff"
    pypi = "reportseff/reportseff-2.7.2.tar.gz"

    license("MIT")

    version("2.7.2", sha256="63cf99ceb0111de511636b214ade937c6c1b8444531e8026dbc34ddf92049c41")

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-click@6.7:", type=("build", "run"))
    depends_on("py-importlib-metadata@4.8.2:4", when="^python@:3.7", type=("build", "run"))
