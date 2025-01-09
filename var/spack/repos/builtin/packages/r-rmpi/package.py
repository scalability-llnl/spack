# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRmpi(RPackage):
    """Interface (Wrapper) to MPI (Message-Passing Interface).

    An interface (wrapper) to MPI APIs. It also provides interactive R manager
    and worker environment."""

    cran = "Rmpi"

    version("0.7-2", sha256="8591fa9f50de52535a32b36e7ed142c6ca4e03fdfdbef79a1e27a63ed5322eef")
    version("0.7-1", sha256="17dae27dea9317aacabc2255dfcf2538fb3195472cedd521256ced9a20dd2dc1")
    version("0.6-9.2", sha256="358ac1af97402e676f209261a231f36a35e60f0301edf8ca53dac11af3c3bd1a")
    version("0.6-9", sha256="b2e1eac3e56f6b26c7ce744b29d8994ab6507ac88df64ebbb5af439414651ee6")
    version("0.6-8", sha256="9b453ce3bd7284eda33493a0e47bf16db6719e3c48ac5f69deac6746f5438d96")
    version("0.6-6", sha256="d8fc09ad38264697caa86079885a7a1098921a3116d5a77a62022b9508f8a63a")

    depends_on("r@2.15.1:", type=("build", "run"))
    depends_on("mpi")

    # The following MPI types are not supported
    conflicts("^[virtuals=mpi] intel-mpi")
    conflicts("^[virtuals=mpi] intel-parallel-studio")
    conflicts("^[virtuals=mpi] mvapich2")
    conflicts("^[virtuals=mpi] spectrum-mpi")

    # Rmpi's Open MPI implementation depends on v4.x ORTE runtime environment
    conflicts("^[virtuals=mpi] openmpi@5:")

    def configure_args(self):
        spec = self.spec

        mpi_name = spec["mpi"].name

        # The type of MPI. Supported values are:
        # OPENMPI, LAM, MPICH, MPICH2, or CRAY
        if mpi_name == "openmpi":
            rmpi_type = "OPENMPI"
        elif mpi_name == "mpich":
            rmpi_type = "MPICH2"
        else:
            raise InstallError("Unsupported MPI type")

        return [
            "--with-Rmpi-type={0}".format(rmpi_type),
            "--with-mpi={0}".format(spec["mpi"].prefix),
        ]
