# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyParasail(PythonPackage):
    """Python Bindings for the Parasail C Library. Parasail is a SIMD C (C99)
    library containing implementations of the Smith-Waterman (local),
    Needleman-Wunsch (global), and semi-global pairwise sequence alignment
    algorithms."""

    homepage = "https://github.com/jeffdaily/parasail-python"
    pypi = "parasail/parasail-1.3.3.tar.gz"

    license("LiLiQ-R-1.1")

    version("1.3.3", sha256="06f05066d9cf624c0b043f51a1e9d2964154e1edd0f9843e0838f32073e576f8")

    depends_on("perl", type="build")
    depends_on("m4", type="build")
    depends_on("libtool", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
