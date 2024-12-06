# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IntelParallelStudio(Package):
    """Intel Parallel Studio."""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"
    url = "http://tec/16225/parallel_studio_xe_2020_cluster_edition.tgz"

    version("cluster.2020.0", sha256="b1d3e3e425b2e44a06760ff173104bdf")

    provides("mpi@:3")
    provides("scalapack")
    provides("blas", "lapack")
