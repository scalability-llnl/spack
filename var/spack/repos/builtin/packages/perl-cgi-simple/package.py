# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCgiSimple(PerlPackage):
    """A Simple totally OO CGI interface that is CGI.pm compliant"""

    homepage = "https://metacpan.org/pod/CGI::Simple"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MANWAR/CGI-Simple-1.281.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.281", sha256="4d58103fdfa5c8e1ed076b15d5cafb7001b2886cb3396f00564a881eb324e5a7")

    depends_on("perl-test-exception", type=("build", "test"))
    depends_on("perl-test-nowarnings", type=("build", "test"))
