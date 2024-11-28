# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCatalystPluginCache(PerlPackage):
    """Flexible caching support for Catalyst."""

    homepage = "https://metacpan.org/pod/Catalyst::Plugin::Cache"
    url = "https://cpan.metacpan.org/authors/id/B/BO/BOBTFISH/Catalyst-Plugin-Cache-0.12.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.12", sha256="295fed449c9324b06578fd468e3391e04fbf64ad24376a004408d1bc6f5443e0")

    depends_on("perl-catalyst-runtime", type=("build", "run", "test"))
    depends_on("perl-mro-compat", type=("build", "run", "test"))
    depends_on("perl-task-weaken", type=("build", "run", "test"))
    depends_on("perl-test-deep", type=("build", "link"))
    depends_on("perl-test-exception", type=("build", "link"))
    depends_on("perl-class-accessor", type=("build", "test"))
