# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyIntelOpenmp(PythonPackage):
    """Intel OpenMP* Runtime Library x86_64 dynamic libraries
    for macOS*. Intel OpenMP* Runtime Library provides OpenMP
    API specification support in Intel C Compiler, Intel C++
    Compiler and Intel Fortran Compiler. It helps to improve
    performance by creating multithreaded software using shared
    memory and running on multi-core processor systems."""

    homepage = "https://pypi.org/project/intel-openmp/"

    if sys.platform.startswith("linux"):
        version(
            "2021.1.2",
            url="https://pypi.io/packages/py2.py3/i/intel-openmp/intel_openmp-2021.1.2-py2.py3-none-manylinux1_x86_64.whl",
            sha256="8796797ecae99f39b27065e4a7f1f435e2ca08afba654ca57a77a2717f864dca",
        )

    if sys.platform.startswith("darwin"):
        version(
            "2021.1.2",
            url="https://pypi.io/packages/py2.py3/i/intel-openmp/intel_openmp-2021.1.2-py2.py3-none-macosx_10_15_x86_64.whl",
            sha256="2af893738b4b06cb0183746f2992169111031340b59c84a0fd4dec1ed66b80f2",
        )
