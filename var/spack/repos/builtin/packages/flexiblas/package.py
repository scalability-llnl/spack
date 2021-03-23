# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Flexiblas(CMakePackage):
    """A BLAS and LAPACK wrapper library with runtime exchangable backends
    """

    homepage = "https://www.mpi-magdeburg.mpg.de/projects/flexiblas"
    url      = "https://csc.mpi-magdeburg.mpg.de/mpcsc/software/flexiblas/flexiblas-3.0.3.tar.gz"

    version('3.0.4', sha256='50a88f2e88994dda91b2a2621850afd9654b3b84820e737e335687a46751be5c')
    version('3.0.3', sha256='926ab31cf56f0618aec34da85314f3b48b6deb661b4e9d6e6a99dc37872b5341')

    # virtual dependency
    provides('blas')
    provides('lapack')
