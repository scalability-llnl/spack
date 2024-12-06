# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlUniversalCan(PerlPackage):
    """Work around buggy code calling UNIVERSAL::can() as a function"""

    homepage = "https://metacpan.org/pod/UNIVERSAL::can"
    url = "https://cpan.metacpan.org/authors/id/C/CH/CHROMATIC/UNIVERSAL-can-1.20140328.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version(
        "1.20140328", sha256="522da9f274786fe2cba99bc77cc1c81d2161947903d7fad10bd62dfb7f11990f"
    )

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
