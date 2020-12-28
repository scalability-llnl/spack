# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRandomfieldsutils(RPackage):
    """Various utilities are provided that might be used in spatial statistics
       and elsewhere. It delivers a method for solving linear equations that
       checks the sparsity of the matrix before any algorithm is used.
       Furthermore, it includes the Struve functions."""

    homepage = "https://cloud.r-project.org/package=RandomFieldsUtils"
    url      = "https://cloud.r-project.org/src/contrib/RandomFieldsUtils_0.5.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RandomFieldsUtils"

    version('0.5.3', sha256='ea823cba2e254a9f534efb4b772c0aeef2039ee9ef99744e077b969a87f8031d')
    version('0.5.1', sha256='a95aab4e2025c4247503ff513570a65aa3c8e63cb7ce2979c9317a2798dfaca2')

    depends_on('r@3.0:', type=('build', 'run'))
