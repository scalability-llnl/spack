# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelStacktraceAshtml(PerlPackage):
    """Displays stack trace in HTML"""

    homepage = "https://metacpan.org/pod/Devel::StackTrace::AsHTML"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MIYAGAWA/Devel-StackTrace-AsHTML-0.15.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.15", sha256="6283dbe2197e2f20009cc4b449997742169cdd951bfc44cbc6e62c2a962d3147")

    depends_on("perl-devel-stacktrace", type=("build", "run", "test"))
