# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mawk(AutotoolsPackage):
    """mawk is an interpreter for the AWK Programming Language."""

    homepage = "http://invisible-island.net/mawk/mawk.html"
    url      = "http://invisible-mirror.net/archives/mawk/mawk-1.3.4.tgz"

    version('1.3.4-20171017', sha256='db17115d1ed18ed1607c8b93291db9ccd4fe5e0f30d2928c3c5d127b23ec9e5b')
    version('1.3.4', sha256='2f2ab8831c441a5793ad333193c888c9ba29c900f009aa23c9fffc100c405925')

    provides('awk')
