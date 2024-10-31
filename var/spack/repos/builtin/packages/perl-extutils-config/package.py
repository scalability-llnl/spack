# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsConfig(PerlPackage):
    """ExtUtils::Config - A wrapper for perl's configuration"""

    homepage = "https://metacpan.org/pod/ExtUtils::Config"
    url = "https://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-Config-0.008.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.010", sha256="82e7e4e90cbe380e152f5de6e3e403746982d502dd30197a123652e46610c66d")
    version("0.009", sha256="4ef84e73aad50a3be332885d2a3b12f3cab1b1e0bad24e88297a123b4f39f3ce")
    version("0.008", sha256="ae5104f634650dce8a79b7ed13fb59d67a39c213a6776cfdaa3ee749e62f1a8c")
