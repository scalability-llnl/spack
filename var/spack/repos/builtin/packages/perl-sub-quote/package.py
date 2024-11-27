# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlSubQuote(PerlPackage):
    """Sub::Quote - Efficient generation of subroutines via string eval"""

    homepage = "https://metacpan.org/pod/Sub::Quote"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Sub-Quote-2.006006.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.006008", sha256="94bebd500af55762e83ea2f2bc594d87af828072370c7110c60c238a800d15b2")
    version("2.006006", sha256="6e4e2af42388fa6d2609e0e82417de7cc6be47223f576592c656c73c7524d89d")

    depends_on("perl-scalar-list-utils", type=("build", "run"))
