# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lwm2(AutotoolsPackage):
    """LWM2: Light Weight Measurement Module.  This is a PMPI module
    that can collect a number of time-sliced MPI and POSIX I/O
    measurements from a program.
    """

    homepage = "https://jay.grs.rwth-aachen.de/redmine/projects/lwm2"
    hg = "https://jay.grs.rwth-aachen.de/hg/lwm2"

    version("torus", revision="torus")

    depends_on("papi")
    depends_on("mpi")
