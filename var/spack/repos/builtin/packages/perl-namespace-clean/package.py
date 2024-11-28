# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNamespaceClean(PerlPackage):
    """Keep imports and functions out of your namespace."""

    homepage = "https://metacpan.org/pod/namespace::clean"
    url = "http://search.cpan.org/CPAN/authors/id/R/RI/RIBASUSHI/namespace-clean-0.27.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.27", sha256="8a10a83c3e183dc78f9e7b7aa4d09b47c11fb4e7d3a33b9a12912fd22e31af9d")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-b-hooks-endofscope@0.12:", type=("build", "run", "test"))
    depends_on("perl-package-stash@0.23:", type=("build", "run", "test"))
