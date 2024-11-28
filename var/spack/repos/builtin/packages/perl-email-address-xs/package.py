# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlEmailAddressXs(PerlPackage):
    """Parse and format RFC 5322 email addresses and groups"""

    homepage = "https://metacpan.org/pod/Email::Address::XS"
    url = "https://cpan.metacpan.org/authors/id/P/PA/PALI/Email-Address-XS-1.05.tar.gz"

    maintainers("EbiArnie")

    version("1.05", sha256="1510b7f10d67201037cd50d22c9d6b26eeca55ededa4cdb46bbca27e59a4ea16")

    depends_on("c", type="build")  # generated

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
