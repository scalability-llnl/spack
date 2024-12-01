# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Netgauge(AutotoolsPackage):
    """Netgauge is a high-precision network parameter measurement
    tool. It supports benchmarking of many different network protocols
    and communication patterns. The main focus lies on accuracy,
    statistical analysis and easy extensibility.
    """

    homepage = "http://unixer.de/research/netgauge/"
    url = "http://unixer.de/research/netgauge/netgauge-2.4.6.tar.gz"

    license("BSD-3-Clause-Open-MPI")

    version("2.4.6", sha256="dc9398e4e042efec70881f2c7074ff18cc5b74bc5ffc4b8a4aaf813b39f83444")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("mpi")

    def configure_args(self):
        args = []
        args.append("MPICC=%s" % os.path.basename(self.spec["mpi"].mpicc))
        args.append("MPICXX=%s" % os.path.basename(self.spec["mpi"].mpicxx))
        return args
