# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStringNumeric(PerlPackage):
    """Determine whether a string represents a numeric value"""

    homepage = "https://metacpan.org/pod/String::Numeric"
    url = "https://cpan.metacpan.org/authors/id/C/CH/CHANSEN/String-Numeric-0.9.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.9", sha256="b992b6611a070e8cd887bc1c7409f22443c115e44245a5c67fb43535b5e0cfdb")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-test-exception", type=("build", "link"))
