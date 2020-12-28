# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRmpi(RPackage):
    """An interface (wrapper) to MPI APIs. It also provides interactive R
       manager and worker environment."""

    homepage = "http://www.stats.uwo.ca/faculty/yu/Rmpi"
    url      = "https://cloud.r-project.org/src/contrib/Rmpi_0.6-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Rmpi"

    version('0.6-9', sha256='b2e1eac3e56f6b26c7ce744b29d8994ab6507ac88df64ebbb5af439414651ee6')
    version('0.6-8', sha256='9b453ce3bd7284eda33493a0e47bf16db6719e3c48ac5f69deac6746f5438d96')
    version('0.6-6', sha256='d8fc09ad38264697caa86079885a7a1098921a3116d5a77a62022b9508f8a63a')

    depends_on('r@2.15.1:', type=('build', 'run'))
    depends_on('mpi')

    # The following MPI types are not supported
    conflicts('^intel-mpi')
    conflicts('^intel-parallel-studio')
    conflicts('^mvapich2')
    conflicts('^spectrum-mpi')

    def configure_args(self):
        spec = self.spec

        mpi_name = spec['mpi'].name

        # The type of MPI. Supported values are:
        # OPENMPI, LAM, MPICH, MPICH2, or CRAY
        if mpi_name == 'openmpi':
            rmpi_type = 'OPENMPI'
        elif mpi_name == 'mpich':
            rmpi_type = 'MPICH2'
        else:
            raise InstallError('Unsupported MPI type')

        return [
            '--with-Rmpi-type={0}'.format(rmpi_type),
            '--with-mpi={0}'.format(spec['mpi'].prefix),
        ]
