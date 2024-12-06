# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlUriFind(PerlPackage):
    """Find URIs in arbitrary text"""

    homepage = "https://metacpan.org/pod/URI::Find"
    url = "https://cpan.metacpan.org/authors/id/M/MS/MSCHWERN/URI-Find-20160806.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("20160806", sha256="e213a425a51b5f55324211f37909d78749d0bacdea259ba51a9855d0d19663d6")

    depends_on("perl@5.8.8:", type=("build", "link", "run", "test"))
    depends_on("perl-uri@1.60:", type=("build", "run", "test"))
