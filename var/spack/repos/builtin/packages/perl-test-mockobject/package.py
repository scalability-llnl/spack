# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestMockobject(PerlPackage):
    """Perl extension for emulating troublesome interfaces"""

    homepage = "https://metacpan.org/pod/Test::MockObject"
    url = "https://cpan.metacpan.org/authors/id/C/CH/CHROMATIC/Test-MockObject-1.20200122.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version(
        "1.20200122", sha256="2b7f80da87f5a6fe0360d9ee521051053017442c3a26e85db68dfac9f8307623"
    )

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-test-exception@0.31:", type=("build", "test"))
    depends_on("perl-test-warn@0.23:", type=("build", "test"))
    depends_on("perl-universal-can@1.20110617:", type=("build", "run", "test"))
    depends_on("perl-universal-isa@1.20110614:", type=("build", "run", "test"))
