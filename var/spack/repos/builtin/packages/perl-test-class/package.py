# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestClass(PerlPackage):
    """Easily create test classes in an xUnit/JUnit style"""

    homepage = "https://metacpan.org/pod/Test::Class"
    url = "https://cpan.metacpan.org/authors/id/S/SZ/SZABGAB/Test-Class-0.52.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.52", sha256="40c1b1d388f0a8674769c27529f0cc3634ca0fd9d8f72b196c0531611934bc82")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-module-runtime", type=("build", "run", "test"))
    depends_on("perl-mro-compat@0.11:", type=("build", "run", "test"))
    depends_on("perl-test-exception@0.25:", type=("build", "test"))
    depends_on("perl-try-tiny", type=("build", "run", "test"))
