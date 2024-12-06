# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pidx(CMakePackage):
    """PIDX Parallel I/O Library.

    PIDX is an efficient parallel I/O library that reads and writes
    multiresolution IDX data files.
    """

    homepage = "http://www.cedmav.com/pidx"
    git = "https://github.com/sci-visus/PIDX.git"

    license("CC-BY-NC-ND-4.0")

    version("1.0", commit="6afa1cf71d1c41263296dc049c8fabaf73c296da")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8.4:", type="build")
    depends_on("mpi")
