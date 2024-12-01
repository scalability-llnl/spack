# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnbc(AutotoolsPackage):
    """LibNBC is a prototypic implementation of a nonblocking
    interface for MPI collective operations. Based on ANSI C and
    MPI-1, it supports all MPI-1 collective operations in a
    nonblocking manner. LibNBC is distributed under the BSD license.
    """

    homepage = "http://unixer.de/research/nbcoll/libnbc/"
    url = "http://unixer.de/research/nbcoll/libnbc/libNBC-1.1.1.tar.gz"

    license("BSD-3-Clause-Open-MPI")

    version("1.1.1", sha256="63aa5f75f84c191da0688cb551ebd0e9e46928edfba350b2a534eb0c704dd9c3")

    depends_on("c", type="build")  # generated

    depends_on("mpi")
