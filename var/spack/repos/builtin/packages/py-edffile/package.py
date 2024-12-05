# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEdffile(PythonPackage):
    """Generic class for Edf files manipulation."""

    homepage = "https://github.com/vasole/pymca/blob/master/PyMca5/PyMcaIO/EdfFile.py"
    git = "https://github.com/conda-forge/edffile-feedstock.git"

    license("BSD-3-Clause")

    version("5.0.0", commit="be5ab4199db9f8209c59e31874934b8536b52301")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))

    build_directory = "recipe/src"
