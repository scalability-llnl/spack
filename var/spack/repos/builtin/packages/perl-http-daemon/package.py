# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpDaemon(PerlPackage):
    """A simple http server class"""

    homepage = "https://metacpan.org/pod/HTTP::Daemon"
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Daemon-6.16.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("6.16", sha256="b38d092725e6fa4e0c4dc2a47e157070491bafa0dbe16c78a358e806aa7e173d")
    version("6.01", sha256="43fd867742701a3f9fcc7bd59838ab72c6490c0ebaf66901068ec6997514adc2")

    depends_on("perl-lwp-mediatypes", type=("build", "run"))
    depends_on("perl-http-message", type=("build", "run"))
    depends_on("perl-http-date", type=("build", "run"))
    depends_on("perl-module-build-tiny", type="build")

    def url_for_version(self, version):
        if self.spec.satisfies("@6.02:"):
            return (
                f"https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Daemon-{version}.tar.gz"
            )
        elif self.spec.satisfies("@6.05"):
            return f"https://cpan.metacpan.org/authors/id/E/ET/ETHER/HTTP-Daemon-{version}.tar.gz"
        else:
            return f"http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/HTTP-Daemon-{version}.tar.gz"
