# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestTimeHires(PerlPackage):
    """Drop-in replacement for Test::Time to work with Time::HiRes"""

    homepage = "https://metacpan.org/pod/Test::Time::HiRes"
    url = "https://cpan.metacpan.org/authors/id/M/MJ/MJEMMESON/Test-Time-HiRes-0.05.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.05", sha256="c9d692fdb7aed618c54a9d38f27edea148874421281b571b9686d2c5a5a8ff63")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-module-build-tiny@0.034:", type=("build"))
    depends_on("perl-test-time@0.07:", type=("build", "run", "test"))
