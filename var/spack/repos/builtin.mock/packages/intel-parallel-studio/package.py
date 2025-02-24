# Copyright Spack Project Developers. See COPYRIGHT file for details.
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
