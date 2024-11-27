# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPypeflow(PythonPackage):
    """pypeFLOW is light weight and reusable make / flow data process
    library written in Python."""

    homepage = "https://github.com/PacificBiosciences/pypeFLOW"
    git = "https://github.com/PacificBiosciences/pypeFLOW.git"

    license("BSD-3-Clause-Clear")

    version("2017-05-04", commit="f23a1b290876bbdf130611000934ae4247158073")

    depends_on("py-setuptools", type="build")
    depends_on("py-networkx@1.7:1.11", type=["build", "run"])
