# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IndirectMpich(Package):
    """Test case for a package that depends on MPI and one of its
    dependencies requires a *particular version* of MPI.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/indirect_mpich-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("mpi")
    depends_on("direct-mpich")
