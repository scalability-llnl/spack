# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Hazelcast(MavenPackage):
    """Hazelcast is an open-source distributed in-memory data
     store and computation platform. It provides a wide variety
     of distributed data structures and concurrency primitives."""

    homepage = "http://www.hazelcast.com/"
    url      = "https://github.com/hazelcast/hazelcast/archive/v3.12.8.tar.gz"

    version('4.0.2', sha256='4f01682583ae6603365ac7a24c568d7598cc3c1cbd736e5c6ed98bd75e39ffa3')
    version('4.0.1', sha256='c9c7d5cbcf70c5e1eb72890df2b4104639f7543f11c6ac5d3e80cd2d4a0d2181')
    version('3.12.8', sha256='65d0e131fc993f9517e8ce9ae5af9515f1b8038304abaaf9da535bdef1d71726')
    version('3.12.7', sha256='0747de968082bc50202f825b4010be28a3885b3dbcee4b83cbe21b2f8b26a7e0')
    version('3.11.7', sha256='c9f636b8813027d4cc24459bd27740549f89b4f11f62a868079bcb5b41d9b2bb')

    depends_on('java@8:', type=('build', 'run'))
