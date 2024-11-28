# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlUniversalIsa(PerlPackage):
    """Attempt to recover from people calling UNIVERSAL::isa as a function"""

    homepage = "https://metacpan.org/pod/UNIVERSAL::isa"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/UNIVERSAL-isa-1.20171012.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version(
        "1.20171012", sha256="d16956036cb01c819dec7d294f6ef891be0bb64876989601354b293164da7f2b"
    )

    depends_on("perl@5.6.2:", type=("build", "link", "run", "test"))
