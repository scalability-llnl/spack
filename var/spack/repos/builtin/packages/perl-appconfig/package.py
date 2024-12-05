# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlAppconfig(PerlPackage):
    """AppConfig - Perl5 module for reading configuration files and parsing
    command line arguments."""

    homepage = "https://metacpan.org/pod/AppConfig"
    url = "https://cpan.metacpan.org/authors/id/N/NE/NEILB/AppConfig-1.71.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.71", sha256="1177027025ecb09ee64d9f9f255615c04db5e14f7536c344af632032eb887b0f")
