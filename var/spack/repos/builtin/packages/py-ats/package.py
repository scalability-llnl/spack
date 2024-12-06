# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAts(PythonPackage):
    """ATS - Automated Testing System - is an open-source, Python-based tool
    for automating the running of tests of an application across a broad range
    of high performance computers."""

    homepage = "https://github.com/LLNL/ATS"
    git = "https://github.com/LLNL/ATS.git"

    maintainers("white238")

    license("MIT")

    version("main", branch="main")
    version("7.0.105", tag="7.0.105", commit="3a3461061d4493a002018f5bb3715db702212f72")
    version("7.0.100", tag="7.0.100", commit="202c18d11b8f1c14f1a3361a6e45c9e4f83a3fa1")
    version("7.0.5", tag="7.0.5", commit="86b0b18b96b179f97008393170f5e5bc95118867")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # TODO: Add flux variant when Flux functionality works in ATS

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-setuptools", type="build")
