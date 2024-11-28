# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCatalystViewJson(PerlPackage):
    """JSON view for your data"""

    homepage = "https://metacpan.org/pod/Catalyst::View::JSON"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Catalyst-View-JSON-0.37.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.37", sha256="c5da3f6e8a77b1c99855de37d58802c0b194e29a7d86c60ed3831cfdd59f9dec")

    depends_on("perl-catalyst-runtime", type=("build", "run", "test"))
    depends_on("perl-json-maybexs@1.003000:", type=("build", "run", "test"))
    depends_on("perl-mro-compat", type=("build", "run", "test"))
