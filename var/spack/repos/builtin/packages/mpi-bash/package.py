# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MpiBash(AutotoolsPackage):
    """Parallel scripting right from the Bourne-Again Shell (Bash)"""

    homepage = "https://github.com/lanl/MPI-Bash"
    url      = "https://github.com/lanl/MPI-Bash/releases/download/v1.2/mpibash-1.2.tar.gz"

    version('1.2', sha256='5c2faaa74464111205dbae4799bd89c2425810ec3708d004237b42d620c8be57')

    depends_on('bash@4.4:')
    # uses MPI_Exscan which is in MPI-1.2 and later
    depends_on('mpi@1.2:')

    depends_on('libcircle')

    def configure_args(self):
        args = [
            "--with-bashdir={0}".format(self.spec['bash'].prefix.include.bash),
            "CC={0}".format(self.spec['mpi'].mpicc)
        ]
        return args
