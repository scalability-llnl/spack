# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHookLexwrap(PerlPackage):
    """Lexically scoped subroutine wrappers"""

    homepage = "https://metacpan.org/pod/Hook::LexWrap"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Hook-LexWrap-0.26.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.26", sha256="b60bdc5f98f94f9294b06adef82b1d996da192d5f183f9f434b610fd1137ec2d")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
