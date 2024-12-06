# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLibwwwPerl(PerlPackage):
    """The libwww-perl collection is a set of Perl modules which provides
    a simple and consistent application programming interface to the
    World-Wide Web. The main focus of the library is to provide classes and
    functions that allow you to write WWW clients."""

    homepage = "https://github.com/libwww-perl/libwww-perl"
    url = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/libwww-perl-6.33.tar.gz"

    license("Artistic-1.0")

    version("6.68", sha256="42784a5869855ee08522dfb1d30fccf98ca4ddefa8c6c1bcb0d68a0adceb7f01")
    version("6.33", sha256="97417386f11f007ae129fe155b82fd8969473ce396a971a664c8ae6850c69b99")
    version("6.29", sha256="4c6f2697999d2d0e6436b584116b12b30dc39990ec0622751c1a6cec2c0e6662")

    depends_on("perl-clone", type=("build", "run"))
    depends_on("perl-encode-locale", type=("build", "run"))
    depends_on("perl-file-listing", type=("build", "run"))
    depends_on("perl-html-parser", type=("build", "run"))
    depends_on("perl-http-cookies", type=("build", "run"))
    depends_on("perl-http-daemon", type=("build", "run"))
    depends_on("perl-http-date", type=("build", "run"))
    depends_on("perl-http-message", type=("build", "run"))
    depends_on("perl-http-negotiate", type=("build", "run"))
    depends_on("perl-lwp-mediatypes", type=("build", "run"))
    depends_on("perl-net-http", type=("build", "run"))
    depends_on("perl-try-tiny", type=("build", "run"))
    depends_on("perl-uri", type=("build", "run"))
    depends_on("perl-www-robotrules", type=("build", "run"))
