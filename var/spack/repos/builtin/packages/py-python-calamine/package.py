# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonCalamine(PythonPackage):
    """Python binding for Rust's library for reading excel and odf file - calamine."""

    homepage = "https://github.com/dimastbk/python-calamine"
    pypi = "python_calamine/python_calamine-0.1.7.tar.gz"

    license("MIT")

    version("0.1.7", sha256="57199dc84522001bdefd0e87e6c50c5a88bf3425dbc3d8fb52c0dec77c218ba2")

    depends_on("py-maturin@1", type="build")
