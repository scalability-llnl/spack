# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# See the Spack documentation for more information on packaging.

from spack.package import *


class RExpint(RPackage):
    """expint: Exponential Integral and Incomplete Gamma Function"""

    homepage = "https://cloud.r-project.org/package=expint"
    url      = "https://cloud.r-project.org/src/contrib/expint_0.1-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/expint"

    version('0.1-5', sha256='b03d60938cd6cf615aa3a02b1bf73436785eca89eaff56059ee0807b8244718a')

    depends_on('r@3.3.0:', type=('build', 'run'))
