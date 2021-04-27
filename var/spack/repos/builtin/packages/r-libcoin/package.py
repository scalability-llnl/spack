# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RLibcoin(RPackage):
    """Linear Test Statistics for Permutation Inference

    Basic infrastructure for linear test statistics and permutation
    inference in the framework of Strasser and Weber (1999)
    <http://epub.wu.ac.at/102/>. This package must not be used by end-users.
    CRAN package 'coin' implements all user interfaces and is ready to be used
    by anyone."""

    homepage = "https://cloud.r-project.org/package=libcoin"
    url      = "https://cloud.r-project.org/src/contrib/libcoin_1.0-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/libcoin"

    version('1.0-6', sha256='48afc1415fc89b29e4f2c8b6f6db3cffef1531580e5c806ad7cacf4afe6a4e5a')
    version('1.0-4', sha256='91dcbaa0ab8c2109aa54c3eda29ad0acd67c870efcda208e27acce9d641c09c5')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
