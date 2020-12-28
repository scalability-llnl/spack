# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLog4r(RPackage):
    """logr4 provides an object-oriented logging system that uses an
    API roughly equivalent to log4j and its related variants."""

    homepage = "https://cloud.r-project.org/package=log4r"
    url      = "https://cloud.r-project.org/src/contrib/log4r_0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/log4r"

    version('0.3.0', sha256='8e5d0221298410e48bee9d9a983a23e1834ce88592f9d931471bfdb05f37a691')
    version('0.2', sha256='321bee6babb92376b538624027a36e7d2a6c8edb360aa38ab0a6762dfea9081f')
