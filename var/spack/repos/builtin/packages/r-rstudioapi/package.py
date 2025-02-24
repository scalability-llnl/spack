# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRstudioapi(RPackage):
    """Safely Access the RStudio API.

    Access the RStudio API (if available) and provide informative error
    messages when it's not."""

    cran = "rstudioapi"

    license("MIT")

    version("0.16.0", sha256="74ffa867199e87a54386fbd26919233371f314f73d7338dd4e4695708fed4fe6")
    version("0.14", sha256="469d0987b1ad728a96c363a422fba712a5cebc8b11a5f7e953b4a671044dafc4")
    version("0.13", sha256="aac35bbdcb4a8e8caba943bc8a2b98120e8940b80cd1020224bb1a26ff776d8b")
    version("0.11", sha256="13e07fb7e2eba8cf1d885db2721901d676d219a1042d7ef5d166125e4905306b")
    version("0.10", sha256="80c5aa3063bcab649904cb92f0b164edffa2f6b0e6a8f7ea28ae317b80e1ab96")
    version("0.9.0", sha256="5149a2830ae7134c396ce64764b263cf9f348d4399f53da3804f40d7d5bec13e")
    version("0.7", sha256="a541bc76ef082d2c27e42fd683f8262cb195b1497af3509178d2642870397a8c")
    version("0.6", sha256="da24c6cdb13af1bdf4261671a065dcca4c1b7af1412cb810eb805bf3c5f97bfe")
    version("0.5", sha256="d5f35bf9614ca2a4bc5333bac7a494d81fbe72b34783304f811f8e0abac3f669")
