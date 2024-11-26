# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PerlHttpTiny(PerlPackage):
    """HTTP::Tiny: A small, simple, correct HTTP/1.1 client perl module"""

    homepage = "https://github.com/Perl-Toolchain-Gang/HTTP-Tiny"
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/HTTP-Tiny-0.088.tar.gz"

    maintainers("teaguesterling")

    # Stated: same as perl5
    license("Artistic-1.0-Perl OR GPL-1.0-or-later", checked_by="teaguesterling")

    version("0.088", sha256="7ce6367e861883b6868d6dd86168af33524717d8cc94100c2abf9bd86a82b4d8")
    version("0.086", sha256="c616e0ff9ec808a7a92f47edb7d017fc45ef0c2cddd21a9bab194096cb6b7b32")

    with default_args(type=("build", "run")):
        depends_on("perl-carp")
