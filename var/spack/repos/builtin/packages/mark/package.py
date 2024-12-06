# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Mark(Package):
    """Program MARK, developed and maintained by Gary White (Colorado State
    University) is the most flexible, widely used application currently
    available for parameter estimation using data from marked individuals.

    You will need to download the package yourself, unzip, rename it
    following the guide in http://www.phidot.org/software/mark/rmark/linux/
    Step(1). Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://www.phidot.org/software/mark/index.html"
    manual_download = True

    version(
        "1.0",
        sha256="5422c9444d5fa6b3b22f4a9f2ce41af2072a1a7283f6f9099dc02cc5282696bc",
        expand=False,
    )

    def url_for_version(self, version):
        return "file://{0}/mark".format(os.getcwd())

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("mark", prefix.bin)

        chmod = which("chmod")
        chmod("+x", prefix.bin.mark)
