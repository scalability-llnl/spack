# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestJson(PerlPackage):
    """Test JSON data"""

    homepage = "https://metacpan.org/pod/Test::JSON"
    url = "https://cpan.metacpan.org/authors/id/O/OV/OVID/Test-JSON-0.11.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.11", sha256="07c08ab2fcc12850d1ad54fcf6afe9ad1a25a098310c3e7142af1d3cb821d7b3")

    depends_on("perl-json-any@1.2:", type=("build", "run", "test"))
    depends_on("perl-test-differences@0.47:", type=("build", "run", "test"))
