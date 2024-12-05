# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDateException(PerlPackage):
    """Base exception package as Moo Role for Date::* packages."""

    homepage = "https://metacpan.org/pod/Date::Exception"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MANWAR/Date-Exception-0.08.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("0.08", sha256="329327e1071123b9b50f31e54202c1f48b866a538cb93aeab193e92eb0c847f8")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-moo@2.000000:", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean@0.28:", type=("build", "run", "test"))
    depends_on("perl-throwable@0.200011:", type=("build", "run", "test"))
