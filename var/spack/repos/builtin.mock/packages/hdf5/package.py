# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hdf5(Package):
    homepage = "http://www.llnl.gov"
    url = "http://www.llnl.gov/hdf5-1.0.tar.gz"

    version("2.3", md5="0123456789abcdef0123456789abcdef")

    variant("mpi", default=True, description="Enable mpi")

    depends_on("mpi", when="+mpi")
