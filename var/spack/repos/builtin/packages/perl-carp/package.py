# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlCarp(PerlPackage):
    """Carp - alternative warn and die for modules"""

    homepage = "https://metacpan.org/pod/Carp"
    url = "https://cpan.metacpan.org/authors/id/X/XS/XSAWYERX/Carp-1.50.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.50", sha256="f5273b4e1a6d51b22996c48cb3a3cbc72fd456c4038f5c20b127e2d4bcbcebd9")

    depends_on("perl-extutils-makemaker", type=("build", "run"))
    depends_on("perl-test-more", type=("build", "run"))
