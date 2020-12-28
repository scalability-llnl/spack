# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAcepack(RPackage):
    """ACE and AVAS for Selecting Multiple Regression Transformations."""

    homepage = "https://cloud.r-project.org/package=acepack"
    url      = "https://cloud.r-project.org/src/contrib/acepack_1.4.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/acepack"

    version('1.4.1', sha256='82750507926f02a696f6cc03693e8d4a5ee7e92500c8c15a16a9c12addcd28b9')
