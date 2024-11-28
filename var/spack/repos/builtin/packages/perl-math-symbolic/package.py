# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathSymbolic(PerlPackage):
    """Math::Symbolic - Symbolic calculations."""

    homepage = "https://metacpan.org/pod/Math::Symbolic"
    url = "https://cpan.metacpan.org/authors/id/S/SM/SMUELLER/Math-Symbolic-0.612.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.612", sha256="a9af979956c4c28683c535b5e5da3cde198c0cac2a11b3c9a129da218b3b9c08")

    depends_on("perl-module-build", type="build")
    depends_on("perl-parse-recdescent", type="run")
