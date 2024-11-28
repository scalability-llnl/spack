# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestMocktime(PerlPackage):
    """Replaces actual time with simulated time"""

    homepage = "https://metacpan.org/pod/Test::MockTime"
    url = "https://cpan.metacpan.org/authors/id/D/DD/DDICK/Test-MockTime-0.17.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.17", sha256="3363e118b2606f1d6abc956f22b0d09109772b7086155fb5c9c7f983350602f9")
