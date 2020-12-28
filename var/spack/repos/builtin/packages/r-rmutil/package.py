# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRmutil(RPackage):
    """rmutil: Utilities for Nonlinear Regression and Repeated
       MeasurementsModels"""

    homepage = "http://www.commanster.eu/rcode.html"
    url      = "https://cloud.r-project.org/src/contrib/rmutil_1.1.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rmutil"

    version('1.1.3', sha256='7abaf41e99d1c4a0e4082c4594964ac1421c53b4268116c82fa55aa8bc0582da')

    depends_on('r@1.4:', type=('build', 'run'))
