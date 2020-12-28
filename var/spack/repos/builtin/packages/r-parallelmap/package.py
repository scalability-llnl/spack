# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RParallelmap(RPackage):
    """Unified parallelization framework for multiple back-end, designed for
       internal package and interactive usage. The main operation is a parallel
       "map" over lists. Supports local, multicore, mpi and BatchJobs mode.
       Allows "tagging" of the parallel operation with a level name that can be
       later selected by the user to switch on parallel execution for exactly
       this operation."""

    homepage = "https://github.com/berndbischl/parallelMap"
    url      = "https://cloud.r-project.org/src/contrib/parallelMap_1.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/parallelMap"

    version('1.4', sha256='fb6f15e325f729f1c5218768b17c20909ee857069c6cc5d8df50e1dafe26ed5b')
    version('1.3', sha256='a52d93572c1b85281e41d8e3c2db97dda5fce96c222e04171b4489ec5000cd08')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-bbmisc@1.8:', type=('build', 'run'))
    depends_on('r-checkmate@1.8.0:', type=('build', 'run'))
