# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Fftw(Package):
    """Used to test that a few problematic concretization
    cases with the old concretizer have been solved by the
    new ones.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/fftw-1.0.tar.gz"

    version("2.0", md5="abcdef1234567890abcdef1234567890")
    version("1.0", md5="1234567890abcdef1234567890abcdef")

    variant("mpi", default=False, description="Enable MPI")

    depends_on("mpi", when="+mpi")
