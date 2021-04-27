# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RZip(RPackage):
    """Cross-Platform 'zip' Compression

    Cross-Platform 'zip' Compression Library. A replacement for the 'zip'
    function, that does not require any additional external tools on any
    platform."""

    homepage = "https://github.com/r-lib/zip#readme"
    url      = "https://cloud.r-project.org/src/contrib/zip_2.0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/zip"

    version('2.1.1', sha256='11dd417932296d3a25c53aa8d3b908973c4945a496cc473dd321825dfaaa7c2c')
    version('2.0.3', sha256='4a8cb8e41eb630bbf448a0fd56bcaeb752b8484fef98c6419334edf46401317e')
