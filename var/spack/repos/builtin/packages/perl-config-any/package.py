# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlConfigAny(PerlPackage):
    """Load configuration from different file formats, transparently"""

    homepage = "https://metacpan.org/pod/Config::Any"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Config-Any-0.33.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.33", sha256="c0668eb5f2cd355bf20557f04dc18a25474b7a0bcfa79562e3165d9a3c789333")

    depends_on("perl-module-pluggable", type=("build", "run", "test"))
