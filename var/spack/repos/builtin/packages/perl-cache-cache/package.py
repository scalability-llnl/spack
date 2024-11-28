# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCacheCache(PerlPackage):
    """Extends Cache::SizeAwareMemoryCache"""

    homepage = "https://metacpan.org/pod/Cache::Cache"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Cache-Cache-1.08.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.08", sha256="d2c7fd5dba5dd010b7d8923516890bb6ccf6b5f188ccb69f35cb0fd6c031d1e8")

    depends_on("perl-digest-sha1@2.02:", type=("build", "run", "test"))
    depends_on("perl-error@0.15:", type=("build", "run", "test"))
    depends_on("perl-ipc-sharelite@0.09:", type=("build", "run", "test"))
