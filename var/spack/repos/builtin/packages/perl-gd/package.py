# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGd(PerlPackage):
    """Interface to Gd Graphics Library"""

    homepage = "https://metacpan.org/pod/GD"
    url = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN/GD-2.77.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.81", sha256="21df5d9c5ced9971f661a69d1c80312bc59d27afdba17a242ac2e8c870b635d5")
    version("2.77", sha256="b56c88b8ef3be016ce29bb62dd1f1b6f6b5fbcaa57fea59e9468af6901016fb5")
    version("2.53", sha256="d05d01fe95e581adb3468cf05ab5d405db7497c0fb3ec7ecf23d023705fab7aa")

    depends_on("perl-module-build", type="build")
    depends_on("perl-extutils-makemaker", type=("build", "run"))
    depends_on("perl-extutils-pkgconfig", type=("build", "run"))
    depends_on("libgd")

    def url_for_version(self, version):
        if version <= Version("2.56"):
            url = "http://search.cpan.org/CPAN/authors/id/L/LD/LDS/GD-{0}.tar.gz"
        else:
            url = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN/GD-{0}.tar.gz"
        return url.format(version)
