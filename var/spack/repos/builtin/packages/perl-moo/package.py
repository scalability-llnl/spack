# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlMoo(PerlPackage):
    """Moo - Minimalist Object Orientation (with Moose compatibility)"""

    homepage = "https://metacpan.org/pod/Moo"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Moo-2.005004.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.005005", sha256="fb5a2952649faed07373f220b78004a9c6aba387739133740c1770e9b1f4b108")
    version("2.005004", sha256="e3030b80bd554a66f6b3c27fd53b1b5909d12af05c4c11ece9a58f8d1e478928")

    depends_on("perl-carp", type=("build", "run"))
    depends_on("perl-class-method-modifiers", type=("build", "run"))
    depends_on("perl-exporter-tiny", type=("build", "run"))
    depends_on("perl-role-tiny", type=("build", "run"))
    depends_on("perl-scalar-list-utils", type=("build", "run"))
    depends_on("perl-sub-quote", type=("build", "run"))
