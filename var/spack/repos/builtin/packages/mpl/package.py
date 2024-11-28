# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpl(CMakePackage):
    """A C++17 message passing library based on MPI."""

    homepage = "https://rabauke.github.io/mpl/html/"
    git = "https://github.com/rabauke/mpl.git"
    url = "https://github.com/rabauke/mpl/archive/refs/tags/v0.3.0.tar.gz"
    maintainers("rabauke")

    license("BSD-3-Clause")

    version("develop", branch="master")
    version("0.3.0", tag="v0.3.0", commit="e6bd4926914127f3609a14474aa4a9c4fabbff0b")
    version("0.2.1", tag="v0.2.1", commit="5bee297b453d7b66a803453bfc6884611a36c4d0")
    version("0.2.0", tag="v0.2.0", commit="f322352c93627c1b91d8efb1c4ee2e4873aed016")
    version("0.1", tag="v0.1", commit="970d0f3436ddbfcf2eba12c5bc7f4f7660e433ca")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("mpi")
