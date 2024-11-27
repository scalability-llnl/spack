# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestTime(PerlPackage):
    """Overrides the time() and sleep() core functions for testing"""

    homepage = "https://metacpan.org/pod/Test::Time"
    url = "https://cpan.metacpan.org/authors/id/A/AN/ANATOFUZ/Test-Time-0.092.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.092", sha256="30d90f54ce840893c7ba2cac2a4d1eecd4c9cdf805910c595e3ae89dfd644738")
