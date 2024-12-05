# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestDifferences(PerlPackage):
    """Test strings and data structures and show differences if not ok"""

    homepage = "https://metacpan.org/pod/Test::Differences"
    url = "http://search.cpan.org/CPAN/authors/id/D/DC/DCANTRELL/Test-Differences-0.64.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.71", sha256="cac16a56cd843b0809e5b49199d60d75a8dbad7ca9a08380dbf3f5cc3aaa38d9")
    version("0.69", sha256="18f644fdd4a1fef93ef3f7f67df8e95b593d811899f34bcbbaba4d717222f58f")
    version("0.64", sha256="9f459dd9c2302a0a73e2f5528a0ce7d09d6766f073187ae2c69e603adf2eb276")

    depends_on("perl-module-build", type="build")
    depends_on("perl-capture-tiny", type=("build", "run"))
    depends_on("perl-text-diff", type=("build", "run"))
