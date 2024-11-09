# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpe2(AutotoolsPackage):
    """Message Passing Extensions (MPE): Parallel, shared X window graphics"""

    homepage = "https://www.mcs.anl.gov/research/projects/perfvis/software/MPE/"
    url = "https://ftp.mcs.anl.gov/pub/mpi/mpe/mpe2-1.3.0.tar.gz"

    version("1.3.0", sha256="0faf32f9adab6fd882be30be913089ebf75272f8b5e4a012bb20c54abc21c0be")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch("mpe2.patch")

    depends_on("mpi")
    depends_on("libx11")

    provides("mpe")

    def configure_args(self):
        args = []

        args.append("--enable-mpe_graphics=yes")
        args.append("--disable-f77")
        args.append("--enable-viewers=no")
        args.append("--enable-slog2=no")
        args.append("--with-mpicc=%s" % self.spec["mpi"].mpicc)

        return args
