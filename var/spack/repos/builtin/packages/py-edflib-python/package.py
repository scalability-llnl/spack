# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEdflibPython(PythonPackage):
    """Library to read/write EDF+/BDF+ files written in pure Python by the same
    author as the original EDFlib."""

    homepage = "https://www.teuniz.net/edflib_python/"
    pypi = "EDFlib-Python/EDFlib-Python-1.0.8.tar.gz"
    git = "https://gitlab.com/Teuniz/EDFlib-Python"

    license("BSD-3-Clause")

    version("1.0.8", sha256="42de3b7980809f37fcc44e3cddc837a3237b69b937a81335dd1f9ffaaf3f2e19")

    depends_on("py-setuptools@42:", type="build")

    depends_on("py-numpy@1.17:", type=("build", "run"))
