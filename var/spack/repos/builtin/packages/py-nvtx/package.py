# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNvtx(PythonPackage):
    """PyNVTX - Python code annotation library."""

    homepage = "https://github.com/NVIDIA/nvtx"
    pypi = "nvtx/nvtx-0.2.10.tar.gz"

    license("Apache-2.0")

    version("0.2.10", sha256="58b89cd69079fda1ceef8441eec5c5c189d6a1ff94c090a3afe03aedd0bbd140")

    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("nvtx")
