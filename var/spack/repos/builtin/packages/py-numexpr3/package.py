# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumexpr3(PythonPackage):
    """Numexpr3 is a fast numerical expression evaluator for NumPy. With it,
    expressions that operate on arrays (like "3*a+4*b") are accelerated and
    use less memory than doing the same calculation in Python.
    In addition, its multi-threaded capabilities can make use of all your
    cores, which may accelerate computations, most specially if they are not
    memory-bounded (e.g. those using transcendental functions).
    Compared to NumExpr 2.6, functions have been re-written in a fashion such
    that gcc can auto-vectorize them with SIMD instruction sets such as
    SSE2 or AVX2, if your processor supports them. Use of a newer version of
    gcc such as 5.4 is strongly recommended."""

    homepage = "https://github.com/pydata/numexpr/tree/numexpr-3.0"
    pypi = "numexpr3/numexpr3-3.0.1a1.tar.gz"

    license("BSD-3-Clause")

    version("3.0.1a1", sha256="de06f1b4206704b5bc19ea09b5c94350b97c211c26bc866f275252a8461b87e6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    # TODO: Add CMake build system for better control of passing flags related
    # to CPU ISA.

    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-setuptools@18.2:", type="build")
