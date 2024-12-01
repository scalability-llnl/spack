# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestTrap(PerlPackage):
    """Trap exit codes, exceptions, output, etc."""

    homepage = "https://metacpan.org/pod/Test::Trap"
    url = "https://cpan.metacpan.org/authors/id/E/EB/EBHANSSEN/Test-Trap-v0.3.5.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("v0.3.5", sha256="54f99016562b5b1d72110100f1f2be437178cdf84376f495ffd0376f1d7ecb9a")

    depends_on("perl@5.6.2:", type=("build", "link", "run", "test"))
    depends_on("perl-data-dump", type=("build", "run", "test"))

    def url_for_version(self, version):
        return (
            f"https://cpan.metacpan.org/authors/id/E/EB/EBHANSSEN/Test-Trap-{str(version)}.tar.gz"
        )
