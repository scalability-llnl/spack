# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDotcall64(RPackage):
    """dotCall64: Enhanced Foreign Function Interface Supporting Long
       Vectors."""

    homepage = "https://git.math.uzh.ch/reinhard.furrer/dotCall64"
    url      = "https://cloud.r-project.org/src/contrib/dotCall64_1.0-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/dotCall64"

    version('1.0-0', sha256='69318dc6b8aecc54d4f789c8105e672198363b395f1a764ebaeb54c0473d17ad')

    depends_on('r@3.1:', type=('build', 'run'))
