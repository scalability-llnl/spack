# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAdgoftest(RPackage):
    """Anderson-Darling GoF test with p-value calculation based on Marsaglia's
    2004 paper 'Evaluating the Anderson-Darling Distribution'"""

    homepage = "https://cloud.r-project.org/package=ADGofTest"
    url      = "https://cloud.r-project.org/src/contrib/ADGofTest_0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ADGofTest"

    version('0.3', sha256='9cd9313954f6ecd82480d373f6c5371ca84ab33e3f5c39d972d35cfcf1096846')
