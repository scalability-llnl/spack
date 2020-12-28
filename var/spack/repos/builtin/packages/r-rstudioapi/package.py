# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRstudioapi(RPackage):
    """Access the RStudio API (if available) and provide informative error
    messages when it's not."""

    homepage = "https://cloud.r-project.org/package=rstudioapi"
    url      = "https://cloud.r-project.org/src/contrib/rstudioapi_0.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rstudioapi"

    version('0.11', sha256='13e07fb7e2eba8cf1d885db2721901d676d219a1042d7ef5d166125e4905306b')
    version('0.10', sha256='80c5aa3063bcab649904cb92f0b164edffa2f6b0e6a8f7ea28ae317b80e1ab96')
    version('0.9.0', sha256='5149a2830ae7134c396ce64764b263cf9f348d4399f53da3804f40d7d5bec13e')
    version('0.7', sha256='a541bc76ef082d2c27e42fd683f8262cb195b1497af3509178d2642870397a8c')
    version('0.6', sha256='da24c6cdb13af1bdf4261671a065dcca4c1b7af1412cb810eb805bf3c5f97bfe')
    version('0.5', sha256='d5f35bf9614ca2a4bc5333bac7a494d81fbe72b34783304f811f8e0abac3f669')
