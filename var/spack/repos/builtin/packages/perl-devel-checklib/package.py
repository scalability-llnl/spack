# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelChecklib(PerlPackage):
    """Devel::CheckLib - check that a library is available"""

    homepage = "https://metacpan.org/pod/Devel::CheckLib"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MATTN/Devel-CheckLib-1.16.tar.gz"
    maintainers("snehring")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.16", sha256="869d38c258e646dcef676609f0dd7ca90f085f56cf6fd7001b019a5d5b831fca")
