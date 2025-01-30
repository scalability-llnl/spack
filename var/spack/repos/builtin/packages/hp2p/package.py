# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hp2p(AutotoolsPackage):
    """HP2P (Heavy Peer To Peer) benchmark is a test which performs MPI
    Point-to-Point non-blocking communications between all MPI processes. Its
    goal is to measure the bandwidths and the latencies in a situation where
    the network is busy. This benchmark can help to detect network problems
    like congestions or problems with switches or links.
    """

    homepage = "https://github.com/cea-hpc/hp2p"
    url = "https://github.com/cea-hpc/hp2p/releases/download/4.1/hp2p-4.1.tar.gz"
    git = "https://github.com/cea-hpc/hp2p.git"

    version("4.1", sha256="e74fa1d442f4378a31f4b875760aaad98e23f6942f7de4cc1702ed9e95585c5e")

    depends_on("mpi", type=("build", "link", "run"))

    def configure_args(self):
        mpi = self.spec["mpi"]
        args = [f"CC={mpi.mpicc}", f"CXX={mpi.mpicxx}"]
        return args
