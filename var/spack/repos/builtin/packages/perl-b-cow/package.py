# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBCow(PerlPackage):
    """B::COW additional B helpers to check COW status"""

    homepage = "https://metacpan.org/pod/B::COW"
    url = "https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/B-COW-0.007.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.007", sha256="1290daf227e8b09889a31cf182e29106f1cf9f1a4e9bf7752f9de92ed1158b44")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
