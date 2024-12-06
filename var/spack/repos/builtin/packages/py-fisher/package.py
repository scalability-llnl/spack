# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFisher(PythonPackage):
    """Fisher's Exact Test.

    Simple, fast implementation of Fisher's exact test."""

    homepage = "https://github.com/brentp/fishers_exact_test"
    pypi = "fisher/fisher-0.1.9.tar.gz"

    license("BSD-3-Clause")

    version("0.1.10", sha256="0ec89019e814cf102f33be5674a6205af433711ecb742a7ed5b48896af243523")
    version("0.1.9", sha256="d378b3f7e488e2a679c6d0e5ea1bce17bc931c2bfe8ec8424ee47a74f251968d")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-cython", type="build", when="@0.1.10:")
