# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTester(RPackage):
    """tester allows you to test characteristics of common R objects."""

    homepage = "https://github.com/gastonstat/tester"
    url      = "https://cloud.r-project.org/src/contrib/tester_0.1.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tester"

    version('0.1.7', sha256='b9c645119c21c69450f3d366c911ed92ac7c14ef61652fd676a38fb9d420b5f4')

    depends_on('r@3.0:', type=('build', 'run'))
