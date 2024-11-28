# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCacheMemcached(PerlPackage):
    """Client library for memcached (memory cache daemon)"""

    homepage = "https://metacpan.org/pod/Cache::Memcached"
    url = "https://cpan.metacpan.org/authors/id/D/DO/DORMANDO/Cache-Memcached-1.30.tar.gz"

    maintainers("EbiArnie")

    version("1.30", sha256="31b3c51ec0eaaf03002e2cc8e3d7d5cbe61919cfdada61c008eb9853acac42a9")

    depends_on("perl-string-crc32", type=("build", "run", "test"))
