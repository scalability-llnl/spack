# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Soci(CMakePackage):
    """Official repository of the SOCI - The C++ Database Access Library"""

    homepage = "https://github.com/SOCI/soci"
    url      = "https://github.com/SOCI/soci/archive/4.0.0.tar.gz"

    version('4.0.0', sha256='359b988d8cbe81357835317821919f7e270c0705e41951a92ac1627cb9fe8faf')
    version('3.2.3', sha256='1166664d5d7c4552c4c2abf173f98fa4427fbb454930fd04de3a39782553199e')
    version('3.2.2', sha256='cf1a6130ebdf0b84d246da948874ab1312c317e2ec659ede732b688667c355f4')
