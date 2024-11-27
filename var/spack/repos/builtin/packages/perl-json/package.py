# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlJson(PerlPackage):
    """JSON (JavaScript Object Notation) encoder/decoder"""

    homepage = "https://metacpan.org/pod/JSON"
    url = "http://search.cpan.org/CPAN/authors/id/I/IS/ISHIGAKI/JSON-2.97001.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("4.10", sha256="df8b5143d9a7de99c47b55f1a170bd1f69f711935c186a6dc0ab56dd05758e35")
    version("2.97001", sha256="e277d9385633574923f48c297e1b8acad3170c69fa590e31fa466040fc6f8f5a")

    variant(
        "json-xs",
        default=True,
        description="""Makes the preferred backend JSON::XS available to avoid defaulting to the
        slower JSON::PP""",
    )

    depends_on("perl-json-xs", when="+json-xs", type=("run"))
