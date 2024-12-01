# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPockets(PythonPackage):
    """A collection of helpful Python tools."""

    homepage = "http://pockets.readthedocs.org/"
    pypi = "pockets/pockets-0.9.1.tar.gz"

    license("BSD-3-Clause")

    version("0.9.1", sha256="9320f1a3c6f7a9133fe3b571f283bcf3353cd70249025ae8d618e40e9f7e92b3")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.5.2:", type=("build", "run"))
