# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTaskWeaken(PerlPackage):
    """Ensure that a platform has weaken support"""

    homepage = "https://metacpan.org/pod/Task::Weaken"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Task-Weaken-1.06.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.06", sha256="2383fedb9dbaef646468ea824afbf7c801076720cfba0df2a7a074726dcd66be")
    version("1.04", sha256="67e271c55900fe7889584f911daa946e177bb60c8af44c32f4584b87766af3c4")

    depends_on("perl-module-install", type="build", when="@:1.04")

    def url_for_version(self, version):
        if self.spec.satisfies("@1.05:"):
            return f"https://cpan.metacpan.org/authors/id/E/ET/ETHER/Task-Weaken-{version}.tar.gz"
        else:
            return (
                f"http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Task-Weaken-{version}.tar.gz"
            )
