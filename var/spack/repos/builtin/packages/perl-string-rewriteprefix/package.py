# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStringRewriteprefix(PerlPackage):
    """Rewrite strings based on a set of known prefixes"""

    homepage = "https://metacpan.org/pod/String::RewritePrefix"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/String-RewritePrefix-0.009.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.009", sha256="44918bec96a54af8ca37ca897e436709ec284a07b28516ef3cce4666869646d5")

    depends_on("perl@5.12.0:", type=("build", "link", "run", "test"))
    depends_on("perl-sub-exporter@0.972:", type=("build", "run", "test"))
