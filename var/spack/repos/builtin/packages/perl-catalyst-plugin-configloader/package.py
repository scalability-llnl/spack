# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCatalystPluginConfigloader(PerlPackage):
    """Load config files of various types"""

    homepage = "https://metacpan.org/pod/Catalyst::Plugin::ConfigLoader"
    url = (
        "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Catalyst-Plugin-ConfigLoader-0.35.tar.gz"
    )

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.35", sha256="9e2a698a6f2d046e0dc5e57512929cd423c807d4a36ba3f29e9e5adcd71a1971")

    depends_on("perl-catalyst-runtime@5.7008:", type=("build", "run", "test"))
    depends_on("perl-config-any@0.20:", type=("build", "run", "test"))
    depends_on("perl-data-visitor@0.24:", type=("build", "run", "test"))
    depends_on("perl-mro-compat@0.09:", type=("build", "run", "test"))
