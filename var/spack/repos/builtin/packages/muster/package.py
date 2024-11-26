# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Muster(CMakePackage):
    """The Muster library provides implementations of sequential and
    parallel K-Medoids clustering algorithms. It is intended as a
    general framework for parallel cluster analysis, particularly
    for performance data analysis on systems with very large
    numbers of processes.
    """

    homepage = "https://github.com/llnl/muster"
    url = "https://github.com/llnl/muster/archive/v1.0.tar.gz"

    version("1.0.1", sha256="71e2fcdd7abf7ae5cc648a5f310e1c5369e4889718eab2a045e747c590d2dd71")
    version("1.0", sha256="370a670419e391494fcca0294882ee5f83c5d8af94ca91ac4182235332bd56d6")

    depends_on("cxx", type="build")  # generated

    depends_on("boost+exception+serialization+random")
    depends_on("mpi")
    depends_on("cmake@2.8:", type="build")
