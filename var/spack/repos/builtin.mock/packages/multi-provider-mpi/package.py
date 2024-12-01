# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MultiProviderMpi(Package):
    """This is a fake MPI package used to test packages providing multiple
    virtuals at the same version."""

    homepage = "http://www.spack-fake-mpi.org"
    url = "http://www.spack-fake-mpi.org/downloads/multi-mpi-1.0.tar.gz"

    version("2.0.0", md5="0123456789abcdef0123456789abcdef")
    version("1.10.3", md5="0123456789abcdef0123456789abcdef")
    version("1.10.2", md5="0123456789abcdef0123456789abcdef")
    version("1.10.1", md5="0123456789abcdef0123456789abcdef")
    version("1.10.0", md5="0123456789abcdef0123456789abcdef")
    version("1.8.8", md5="0123456789abcdef0123456789abcdef")
    version("1.6.5", md5="0123456789abcdef0123456789abcdef")

    provides("mpi@3.1", when="@2.0.0")
    provides("mpi@3.0", when="@1.10.3")
    provides("mpi@3.0", when="@1.10.2")
    provides("mpi@3.0", when="@1.10.1")
    provides("mpi@3.0", when="@1.10.0")
    provides("mpi@3.0", when="@1.8.8")
    provides("mpi@2.2", when="@1.6.5")
