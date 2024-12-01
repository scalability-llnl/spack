# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSafeIsa(PerlPackage):
    """Call isa, can, does and DOES safely on things that may not be objects"""

    homepage = "https://metacpan.org/pod/Safe::Isa"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Safe-Isa-1.000010.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.000010", sha256="87f4148aa0ff1d5e652723322eab7dafa3801c967d6f91ac9147a3c467b8a66a")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
