# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimeDurationParse(PerlPackage):
    """Parse string that represents time duration"""

    homepage = "https://metacpan.org/pod/Time::Duration::Parse"
    url = "https://cpan.metacpan.org/authors/id/N/NE/NEILB/Time-Duration-Parse-0.16.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.16", sha256="1084a6463ee2790f99215bd76b135ca45afe2bfa6998fa6fd5470b69e1babc12")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-time-duration", type=("build", "test"))
