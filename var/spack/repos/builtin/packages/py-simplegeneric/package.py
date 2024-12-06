# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySimplegeneric(PythonPackage):
    """Simple generic functions (similar to Python's own len(),
    pickle.dump(), etc.)"""

    pypi = "simplegeneric/simplegeneric-0.8.zip"

    license("ZPL-2.1")

    version("0.8.1", sha256="dc972e06094b9af5b855b3df4a646395e43d1c9d0d39ed345b7393560d0b9173")
    version("0.8", sha256="8c0c4963da2695ba7c0f953f2cdac31d2c41d619fe9419e9d75432f8a231f966")

    depends_on("py-setuptools", type="build")
