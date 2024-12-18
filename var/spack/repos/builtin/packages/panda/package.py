# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Panda(CMakePackage):
    """PANDA: Parallel AdjaceNcy Decomposition Algorithm"""

    homepage = "http://comopt.ifi.uni-heidelberg.de/software/PANDA/index.html"
    url = "http://comopt.ifi.uni-heidelberg.de/software/PANDA/downloads/panda-2016-03-07.tar"

    license("CC-BY-4.0")

    version(
        "2016-03-07", sha256="9fae1544626db417ade7318d26bc43c8af04151b9f7679b6d742dba598762037"
    )

    depends_on("cxx", type="build")  # generated

    # Note: Panda can also be built without MPI support

    depends_on("cmake@2.6.4:", type="build")
    depends_on("mpi")
