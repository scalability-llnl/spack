# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCatalystActionRenderview(PerlPackage):
    """Sensible default end action."""

    homepage = "https://metacpan.org/pod/Catalyst::Action::RenderView"
    url = (
        "https://cpan.metacpan.org/authors/id/B/BO/BOBTFISH/Catalyst-Action-RenderView-0.16.tar.gz"
    )

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.16", sha256="8565203950a057d43ecd64e9593715d565c2fbd8b02c91f43c53b2111acd3948")

    depends_on("perl-catalyst-runtime@5.80030:", type=("build", "run", "test"))
    depends_on("perl-data-visitor@0.24:", type=("build", "run", "test"))
    depends_on("perl-http-request-ascgi", type=("build", "link"))
    depends_on("perl-mro-compat", type=("build", "run", "test"))
