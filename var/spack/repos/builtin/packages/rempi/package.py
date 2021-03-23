# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rempi(AutotoolsPackage):
    """ReMPI is a record-and-replay tool for MPI applications."""
    homepage = "https://github.com/PRUNERS/ReMPI"
    url      = "https://github.com/PRUNERS/ReMPI/releases/download/v1.0.0/ReMPI-1.0.0.tar.gz"

    version("1.1.0", sha256="4fd94fca52311fd19dc04a32547841e6c1c1656b7999b2f76f537d6ec24efccc")
    version("1.0.0", sha256="1cb21f457cf8a04632150156a2ba699dd0c3f81d47e8881a9b943b9bf575fa01")

    depends_on("mpi")
    depends_on("zlib")
    depends_on("autoconf", type='build')
    depends_on("automake", type='build')
    depends_on("libtool", type='build')
    depends_on("libpciaccess", type='link')
