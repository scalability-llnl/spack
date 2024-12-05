# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHashMultivalue(PerlPackage):
    """Store multiple values per key"""

    homepage = "https://metacpan.org/pod/Hash::MultiValue"
    url = "https://cpan.metacpan.org/authors/id/A/AR/ARISTOTLE/Hash-MultiValue-0.16.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.16", sha256="66181df7aa68e2786faf6895c88b18b95c800a8e4e6fb4c07fd176410a3c73f4")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
