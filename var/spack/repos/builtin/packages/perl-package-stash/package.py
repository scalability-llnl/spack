# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPackageStash(PerlPackage):
    """Routines for manipulating stashes"""

    homepage = "https://metacpan.org/pod/Package::Stash"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Package-Stash-0.40.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.40", sha256="5a9722c6d9cb29ee133e5f7b08a5362762a0b5633ff5170642a5b0686e95e066")
    version("0.37", sha256="06ab05388f9130cd377c0e1d3e3bafeed6ef6a1e22104571a9e1d7bfac787b2c")

    depends_on("perl-test-requires", type=("build", "run"))
    depends_on("perl-test-fatal", type=("build", "run"))
    depends_on("perl-module-implementation", type=("build", "run"))
    depends_on("perl-dist-checkconflicts", type=("build", "run"))

    def url_for_version(self, version):
        if self.spec.satisfies("@0.38:"):
            return (
                f"https://cpan.metacpan.org/authors/id/E/ET/ETHER/Package-Stash-{version}.tar.gz"
            )
        else:
            return (
                f"http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Package-Stash-{version}.tar.gz"
            )
